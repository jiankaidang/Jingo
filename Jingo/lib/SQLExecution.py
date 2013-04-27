from django.db import connection, transaction

class SQLExecuter:

	def __init__(self):
		self.cursor = connection.cursor()

	def getInsertString(self, args):
		strValues = ''
		for v in args['values']:
			strValues += '%s, '
		return strValues[:len(strValues)-2]

	def getDeleteString(self, args):
		strValues = ''
		for attr in args['attributes']:
			strValues += attr + '=%s And '
		return strValues[:len(strValues)-4]

	def doInsertData(self, args):
		strValues = self.getInsertString(args)
		self.cursor.execute("Insert Into " + args['table'] + " Values (" + strValues + ")", args['values'])
		transaction.commit_unless_managed()

	def doSelectData(self, args):
		strValues = self.getDeleteString(args)
		#print "Delete From " + args['table'] + " Where " + strValues
		self.cursor.execute("Delete From " + args['table'] + " Where " + strValues, args['values'])
		transaction.commit_unless_managed()