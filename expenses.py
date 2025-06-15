import pyperclip as py
import re
from datetime import datetime 

rawExpensesStr = py.paste()
rawExpenses = re.split(r'\d+\.\t', rawExpensesStr);

class Expense:
	def __init__(self, actualDate, receiver, moreInfo, amount):
		self.actualDate = actualDate;
		self.receiver = receiver;
		self.moreInfo = moreInfo;
		self.amount = amount;
		
class Category:		
	def __init__(self, name, textsInReceiver, textsInMoreInfo = []):
		self.name = name;
		self.textsInReceiver = textsInReceiver;
		self.textsInMoreInfo = textsInMoreInfo;

def parseExpenses(rawExpenses):
  linePattern = re.compile(r"^(.*?)\t(.*?)\t(.*?)\n(-([\d.]+))\t(.*)$");
  moreInfoPattern = re.compile("(.*? (\d{2}\.\d{2}.\d{2,4}) .*)");
  expenses = [];
  for rawExpense in rawExpenses:
    if rawExpense == "":
      continue;
    linePatternResult = linePattern.search(rawExpense);
    if linePatternResult == None:
      print("Skipping line: " + rawExpense);	
    else:
      moreInfoPatternResult = moreInfoPattern.search(linePatternResult.group(3))
      if moreInfoPatternResult == None:
        moreInfo = "";
        actualDate = linePatternResult.group(1);
      else:
        moreInfo = moreInfoPatternResult.group(1);
        actualDate = moreInfoPatternResult.group(2);
        if (len(actualDate) == 8):
          actualDate = linePatternResult.group(1);
      expenses.append(Expense(actualDate, linePatternResult.group(2), moreInfo, float(linePatternResult.group(5))));
  return expenses;

categories = [ 
	Category("Food & Home (Shop)", ["MAXIMA", "RIMI", "MARKET", "Veikals", "MEGO", "BETA", "MULTICOOK LATGALES IELA", "Auglu un darzenu pasau", "TIRGUS"], ["DK Zall"]),
	Category("Food Orders (Wolt)", ["Wolt"]),
	Category("Food for Valja", ["VALENTĪNA BONDARČUKA"]),
	Category("Bistro & Restaurants", ["Aleksandrs-pusdienu", "LIDO", "SENJORITA KUKU", "MCA SIA", "Bistro", "BISTRO", "SIA Cydonia", "GAN BEI", "BAKA", "Rama-vegetarais restor"]),
	Category("Cafe", ["SANITEX", "NARVESEN", "MCDONALDS", "CIRCLE K", "kafejnica", "Kafejnica", "Alma", "KAFIJA", "GUSTAVBEKEREJA", "Bekereja", "12EAT", "GELATO ITALIA"]),
	Category("Pet Shop", ["DINO ZOO", "ZOOCENTRS"]),
	Category("SPA", ["SPA"]),
	Category("Hair Care", ["AMISI"]),
	Category("Flower Shop", ["Taurinzieds"]),
	Category("Taxi (Bolt)", ["BOLT.EU"]),
	Category("Cosmetics", ["DROGAS", "BEAUTYFOR"]),
	Category("Books", ["MnogoKnig", "Gramatnica"]),
	Category("Medical drugs", ["APTIEKA", "WWW.MEDICINASPRECES.LV"]),
	Category("Medical services", ["Traumpunkts"]),
	Category("Transport", ["www.mobilly.lv"]),
	Category("Monay", [], ["NAUDAS IZSN."]),
	Category("Dress", ["PEPCO", "SINSAY"]),
	Category("Sport", ["GERMANS U", "teinisa"]),
	Category("Phone expenses", ["TELE2", "MANS.LMT.LV"]),
	Category("Internet orders", ["AMAZON", "eBay"]),
	Category("Apartment expenses", [ "RĪGAS NAMU PĀRVALDNIEKS SIA", "LATVENERGO AS", "BALTICOM AS" ])
	];
	
categoryOther =	Category("Other", []);

def attachCategoryToExpense(expense):
	for category in categories:
		for textInReceiver in category.textsInReceiver:
			if textInReceiver in expense.receiver:
				expense.category = category;
				return expense;	
		for textInMoreInfo in category.textsInMoreInfo:
			if textInMoreInfo in expense.moreInfo:
				expense.category = category;
				return expense;
	expense.category = categoryOther;
	return expense;					

def attachCategoriesToExpenses(expenses):
	for expense in expenses:
		attachCategoryToExpense(expense);

def groupExpensesByDate(expenses):
	dates = {};
	for expense in expenses:
		dates.setdefault(expense.actualDate, {});
		dateCategories = dates[expense.actualDate];
		dateCategories.setdefault(expense.category, []);
		dateCategories[expense.category].append(expense);
	return dates;	
	
def printExpensesByDates(dates):				
	for date, categories in sorted(dates.items(), key=lambda item: datetime.strptime(item[0], '%d.%m.%Y')):
		print(date);
		for category, expenses in categories.items():
			print(" ", category.name);
			for expense in expenses:
				print(" " * 4, end="");
				printExpense(expense);
   	 		
def printExpense(expense):
	print(expense.amount, expense.receiver);   	 				

def calcTotalsByDate(expenses):
    dates = {};
    for expense in expenses:
        dates.setdefault(expense.actualDate, 0);
        dates[expense.actualDate] = dates[expense.actualDate] + expense.amount;
    return dates;

def calcTotalsByCategory(expenses):
    categories = {};
    for expense in expenses:
        categories.setdefault(expense.category, 0);
        categories[expense.category] = categories[expense.category] + expense.amount;
    return categories;         

def printTotalsByDate(totalsByDate):
    print("Totals By Date");
    for day, total in sorted(totalsByDate.items(), key=lambda kv: kv[1]):
        print(" ", day + ":", f"{total:.2f}");    

def printTotalsByCategory(totalsByCategory):
    print("Totals By Category");
    for category, total in sorted(totalsByCategory.items(), key=lambda kv: kv[1]):
        print(" ", category.name.ljust(21) + ":", f"{total:.2f}");   

def calcAveragesByCategory(expenses, totalDays):
    categories = {};
    for expense in expenses:
        categories.setdefault(expense.category, {});
        datesInCategory = categories[expense.category];
        actualDate = expense.actualDate;
        datesInCategory.setdefault(actualDate, 0);
        datesInCategory[actualDate] = datesInCategory[actualDate] + expense.amount;
    averages = {};
    for category, dates in categories.items():
        averages[category] = sum(dates.values()) / totalDays;    
    return averages;         

def printAveragesByCategory(averagesByCategory):
    print("Averages By Category");
    for category, average in sorted(averagesByCategory.items(), key=lambda kv: kv[1]):
        print(" ", category.name.ljust(21) + ":", f"{average:.2f}"); 
    total = sum(averagesByCategory.values());
    print("Total:", f"{total:.2f}");      

   
expenses = parseExpenses(rawExpenses);
attachCategoriesToExpenses(expenses);
dates = groupExpensesByDate(expenses);
totalsByDate = calcTotalsByDate(expenses);
totalsByCategory = calcTotalsByCategory(expenses);
totalDays = len(dates);
averagesByCategory = calcAveragesByCategory(expenses, totalDays);

printExpensesByDates(dates);
print("");
printTotalsByDate(totalsByDate);
print("");
printTotalsByCategory(totalsByCategory);
print("");
printAveragesByCategory(averagesByCategory);
