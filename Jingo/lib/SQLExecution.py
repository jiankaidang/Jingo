from django.db import connection, transaction

class SQLExecuter:

	def __init__(self):
		self.cursor = connection.cursor()
		
	def dictfetchall(self, cursor):
		#"Returns all rows from a cursor as a dict"
		desc = cursor.description
		return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
	
	def getSQLString(self, args):
		resultset     = {}
		strColumns    = '' 
		strTables     = '' 
		strJoins      = ''
		strConditions = ''
		
		for column in args['columns']:
			strColumns += column + ', '
			
		for table in args['tables']:
			strTables += table + ', '
		
		for join in args['joins']:
			strJoins += join + ' And '
		
		last_logic = 0
		for condition in args['conditions']:
			strConditions += condition['criteria'] + '%s ' + condition['logic'] + ' '
			last_logic     = len(condition['logic']) + 2
			
		resultset['columns']    = strColumns[:len(strColumns)-2]
		resultset['tables']     = strTables[:len(strTables)-2]
		if len(strConditions) == 0:
			resultset['joins']  = strJoins[:len(strJoins)-4]
		else:
			resultset['joins']  = strJoins
		resultset['conditions'] = strConditions[:len(strConditions)-last_logic]
		
		return resultset
	
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

	def doDeleteData(self, args):
		strValues = self.getInsertString(args)
		strSQL    = "Delete From " + args['table'] + " Where " + strValues
		self.cursor.execute(strSQL, args['values'])
		transaction.commit_unless_managed()
		
	def doSelectData(self, args):
		strValues = self.getSQLString(args)
		strSQL    = "Select " + strValues['columns'] + " From " + strValues['tables'] + " "
		strSQL   += "Where " + strValues['joins'] + strValues['conditions']
		print strSQL
		self.cursor.execute(strSQL, args['values'])
		return self.dictfetchall(self.cursor)
		