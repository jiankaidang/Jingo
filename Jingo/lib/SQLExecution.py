from django.db import connection, transaction

class SQLExecuter:

	def __init__(self):
		self.cursor = connection.cursor()

	def getInsertString(self, args):
		strValues = ''
		for v in args['values']:
			strValues += '%s, '
		return strValues[:len(strValues)-2]

	def doInsertData(self, args):
		strValues = self.getInsertString(args)
		self.cursor.execute("Insert Into " + args['table'] + " Values (" + strValues + ")", args['values'])
		transaction.commit_unless_managed()

	def doSelectData(self, args):
		# Data retrieval operation - no commit required
		self.cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
		row = self.cursor.fetchone()
