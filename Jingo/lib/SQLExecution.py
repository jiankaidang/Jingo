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
		strValues  = ''
		last_logic = 0
		for attr in args['attributes']:
			strValues += attr['field'] + '=%s ' + attr['logic'] + ' '
			last_logic = len(attr['logic']) + 1
		return strValues[:len(strValues)-last_logic]
	
	def getUpdateString(self, args):
		result = {}
		strValues  = ''
		for attr in args['attributes']:
			strValues += attr + '=%s, '
		result['fields'] = strValues[:len(strValues) - 2]
		
		strConditions = ''
		last_logic = 0
		for attr in args['conditions']:
			strConditions += attr['field'] + '=%s ' + attr['logic'] + ' '
			last_logic = len(attr['logic']) + 1
		result['conditions'] = strConditions[:len(strConditions) - last_logic]
		
		return result
	
	def doInsertData(self, args):
		strValues = self.getInsertString(args)
		strSQL    = "Insert Into " + args['table'] + " Values (" + strValues + ")"
		#print strSQL
		self.cursor.execute(strSQL, args['values'])
		transaction.commit_unless_managed()

	def doDeleteData(self, args):
		strValues = self.getDeleteString(args)
		strSQL    = "Delete From " + args['table'] + " Where " + strValues
		#print strSQL
		self.cursor.execute(strSQL, args['values'])
		transaction.commit_unless_managed()
	
	def doUpdateData(self, args):
		strValues = self.getUpdateString(args)
		strSQL    = "Update " + args['table'] + " Set " + strValues['fields'] + " Where " + strValues['conditions']
		print strSQL
		self.cursor.execute(strSQL, args['values'])
		transaction.commit_unless_managed()
		
	def doSelectData(self, args):
		strValues = self.getSQLString(args)
		strSQL    = "Select " + strValues['columns'] + " From " + strValues['tables'] + " "
		strSQL   += "Where " + strValues['joins'] + strValues['conditions']
		#print 'do select'
		#print strSQL
		self.cursor.execute(strSQL, args['values'])
		return self.dictfetchall(self.cursor)
	
	def doRawSQL(self, strSQL, args=[]):
		print strSQL
		self.cursor.execute(strSQL, args)
		return self.dictfetchall(self.cursor)