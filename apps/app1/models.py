from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):
	def register(self, formdata):
		errors = []
		if not EMAIL_REGEX.match(formdata['email']):
			errors.append("Invalid email.")
		elif User.objects.filter(email=formdata['email']):
			errors.append("Invalid email.")
		if not formdata['first_name']:
			errors.append("Name field cannot be blank.")
		if not formdata['last_name']:
			errors.append("Name field cannot be blank")
		if len(formdata['password']) < 8:
			errors.append("Password must be more than eight characters.")
		elif not formdata['password'] == formdata['confirm_password']:
			errors.append("Passwords must match.")

		result = {}

		if errors:
			result['registered'] = False
			result['errors'] = errors
		else:
			pw_hash = bcrypt.hashpw(formdata['password'].encode(), bcrypt.gensalt())
			newUser = self.create(first_name=formdata['first_name'], last_name=formdata['last_name'], email=formdata['email'], password=pw_hash)
			result['registered'] = True	
			result['newUser'] = newUser
		return result

	def validateLogin(self, formdata):
		user = self.filter(email=formdata['email'])

		if not user:
			return False
		else:
			current_user = user[0]

		if bcrypt.hashpw(formdata['password'].encode(), current_user.password.encode()) == current_user.password.encode():
			return current_user

		else:
			return False

class User(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()