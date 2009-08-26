#!/usr/bin/env python
'''
Script for recursively checking the permissions of files.

Typical use case: you copied over some files from a FAT partition
and consequently all permissions are set to 777.
This script reports files that are not 644 or more secure
and directorys that are not 755 or more secure.
'''

import os
import stat


def pretty_permission(m):
	'''pretty permission string for stat mode m'''

	r = ['-', 'r']
	w = ['-', 'w']
	x = ['-', 'x']
	s = ''
	s += r[m & stat.S_IRUSR > 0] + w[m & stat.S_IWUSR > 0] + x[m & stat.S_IXUSR > 0]
	s += r[m & stat.S_IRGRP > 0] + w[m & stat.S_IWGRP > 0] + x[m & stat.S_IXGRP > 0]
	s += r[m & stat.S_IROTH > 0] + w[m & stat.S_IWOTH > 0] + x[m & stat.S_IXOTH > 0]
	return s

class PersonaPermission(object):
	'''
	Helper class to contain the permissions assocated to a persona (user, group or other)
	'''
	def __init__(self, r, w, x):
		self.r = bool(r)
		self.w = bool(w)
		self.x = bool(x)
	def __str__(self):
		return ['-', 'r'][self.r] + ['-', 'w'][self.w] + ['-', 'x'][self.x]
	def __repr__(self):
		return "PersonaPermission(r=%s, w=%s, x=%s)" % (self.r, self.w, self.x)

	def __eq__(self, other):
		return self.r == other.r and self.w == other.w and self.x == other.x

	def __ne__(self, other):
		return self.r != other.r or self.w != other.w or self.x != other.x

class Permissions(object):
	'''
	Class for managing user, group and other permissions.
	'''
	def __init__(self, st_mode=0644):
		self.user = PersonaPermission(r=st_mode & stat.S_IRUSR, w=st_mode & stat.S_IWUSR, x=st_mode & stat.S_IXUSR)
		self.group = PersonaPermission(r=st_mode & stat.S_IRGRP, w=st_mode & stat.S_IWGRP, x=st_mode & stat.S_IXGRP)
		self.other = PersonaPermission(r=st_mode & stat.S_IROTH, w=st_mode & stat.S_IWOTH, x=st_mode & stat.S_IXOTH)

	def get_st_mode(self):
		st_mode = self.user.r * stat.S_IRUSR + self.user.w * stat.S_IWUSR + self.user.x * stat.S_IXUSR
		st_mode += self.group.r * stat.S_IRGRP + self.group.w * stat.S_IWGRP + self.group.x * stat.S_IXGRP
		st_mode += self.other.r * stat.S_IROTH + self.other.w * stat.S_IWOTH + self.other.x * stat.S_IXOTH
		return st_mode

	def __str__(self):
		return str(self.user) + str(self.group) + str(self.other)

	def __repr__(self):
		return "Permissions(%s)" % oct(self.get_st_mode())

	def __eq__(self, other):
		return self.user == other.user and self.group == other.group and self.other == other.other
	def __ne__(self, other):
		return self.user != other.user or self.group != other.group or self.other != other.other

	def fix(self, dir_mode=False):
		'''Analyse the permissions and fix them.'''
		# 777 should probably be 644 for files or 755 for dirs
		if self.get_st_mode() == 0777:
			self.group.w = False
			self.other.w = False
			if not dir_mode:
				self.user.x = False
				self.group.x = False
				self.other.x = False
		# Other can have at most the permissions of groups and user.
		for type in ['r', 'w', 'r']:
			self.group.__dict__[type] = self.group.__dict__[type] and self.user.__dict__[type]
			self.other.__dict__[type] = self.other.__dict__[type] and self.group.__dict__[type]
		# Files nor directories should not be writable to group and other.
		self.group.w = False
		self.other.w = False
		# Files should not be executable by group and other.
		if not dir_mode:
			self.group.x = False
			self.other.x = False


class PermissionChecker(object):
	def __init__(self):
		pass

	def check(self, top):
		for root, dirs, files in os.walk(top):
			for f in files:
				f = os.path.join(root, f)
				orig_perm = Permissions(os.stat(f).st_mode)
				sugg_perm = Permissions(os.stat(f).st_mode)
				sugg_perm.fix(dir_mode=False)
				if orig_perm != sugg_perm:
					print '-' + str(orig_perm), '->', '-' + str(sugg_perm), f

			for d in dirs:
				d = os.path.join(root, d)
				orig_perm = Permissions(os.stat(d).st_mode)
				sugg_perm = Permissions(os.stat(d).st_mode)
				sugg_perm.fix(dir_mode=True)
				if orig_perm != sugg_perm:
					print '-' + str(orig_perm), '->', '-' + str(sugg_perm), d



if __name__ == '__main__':
	PermissionChecker().check('.')
