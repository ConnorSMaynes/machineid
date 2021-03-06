import winreg
import os
import platform

__all__ = [
	'get',
]

_machine_id = None


def _get_windows_id():
	# shameless copy: https://stackoverflow.com/questions/36235807/fixed-identifier-for-a-machine-uuid-getnode
	registry = winreg.HKEY_LOCAL_MACHINE
	address = 'SOFTWARE\\Microsoft\\Cryptography'
	keyargs = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
	key = winreg.OpenKey(registry, address, 0, keyargs)
	value = winreg.QueryValueEx(key, 'MachineGuid')
	winreg.CloseKey(key)
	id_ = value[0]
	return id_


def _get_linux_id():
	# ported from go version: https://github.com/denisbrodbeck/machineid/blob/master/id_linux.go
	dbus_fp = '/var/lib/dbus/machine-id'
	dbus_etc_fp = '/etc/machine-id'
	id_ = None
	if os.path.exists(dbus_fp):
		with open(dbus_fp) as f:
			id_ = f.read()
	elif os.path.exists(dbus_etc_fp):
		with open(dbus_etc_fp) as f:
			id_ = f.read()
	if id_:
		return str(id_).strip()


def get():
	global _machine_id
	if _machine_id is None:
		systype = platform.system()
		if systype.lower() == 'windows':
			_machine_id = _get_windows_id()
		elif systype.lower() == 'linux':
			_machine_id = _get_linux_id()
		else:
			raise Exception('System, %s, not supported.' % systype)
	if _machine_id is None:
		raise Exception('A machine id could not be found.')
	return _machine_id
