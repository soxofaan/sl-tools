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

class PermissionChecker(object):
	def __init__(self):
		pass

	def check(self, top):
		for root, dirs, files in os.walk(top):
			for f in files:
				f = os.path.join(root, f)
				m = os.stat(f).st_mode
				# check
				problems = []
				problems += self.check_read_permissions(m)
				problems += self.check_write_permissions(m)
				problems += self.check_file_execute_permissions(m)
				# report
				if len(problems) > 0:
					print oct(m), '-' + pretty_permission(m), f

			for d in dirs:
				d = os.path.join(root, d)
				m = os.stat(f).st_mode
				# check
				problems = []
				problems += self.check_read_permissions(m)
				problems += self.check_write_permissions(m)
				problems += self.check_dir_execute_permissions(m)
				# report
				if len(problems) > 0:
					print oct(m), 'd' + pretty_permission(m), d



	def check_read_permissions(self, st_mode):
		problems = []
		if not st_mode & stat.S_IRUSR and st_mode & stat.S_IRGRP:
			problems.append("not readable for user but readable for group")
		if not st_mode & stat.S_IRUSR and st_mode & stat.S_IROTH:
			problems.append("not readable for user but readable for other")
		return problems

	def check_write_permissions(self, st_mode):
		problems = []
		if st_mode & stat.S_IWGRP:
			problems.append("writable for groups")
		if st_mode & stat.S_IWOTH:
			problems.append("writable for other")
		return problems

	def check_file_execute_permissions(self, st_mode):
		problems = []
		if st_mode & stat.S_IXGRP:
			problems.append("executable for group")
		if st_mode & stat.S_IXOTH:
			problems.append("executable for other")
		return problems

	def check_dir_execute_permissions(self, st_mode):
		problems = []
		if not st_mode & stat.S_IXUSR and st_mode & stat.S_IXGRP:
			problems.append("not executable for user but executable for group")
		if not st_mode & stat.S_IXUSR and st_mode & stat.S_IXOTH:
			problems.append("not executable for user but executable for other")
		return problems




if __name__ == '__main__':
	PermissionChecker().check('.')
