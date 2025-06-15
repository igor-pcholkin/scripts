from hashlib import sha256

def sha256digest(input):
	print(f"'{input}'")
	hbytes = bytes.fromhex(input)
	print(len(hbytes))
	ssha256 = sha256(hbytes)
	return ssha256.hexdigest()

input = '00400920ccc2e4404dcc64603dabcc8f4db685b34137681108100100000000000000000070b000142aacb65ec83fd1c59ad978aa83fa37405f6b0ed1f37ff37acda750982b67f2668c090317646d4df4fd6610'

doubleSha256digest = sha256digest(sha256digest(input))
print(doubleSha256digest)
