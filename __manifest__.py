{
	'name' : 'My Library',
	'summary' : 'Manage books easily',
	'description' : """
		Manage library
		==================
		Description related to library
		""",
	'application' : True,
	'author' : 'Make It Happen',
	'website' : 'https://mih.tn/',
	'version' : '13.0.1',
	'depends' : ['base'],
	'demo' : ['demo.xml'],

	'data' : [
		'security/groups.xml',
		'security/ir.model.access.csv',
		'views/views.xml',
		'views/book_menus.xml',
		'views/library_book.xml'
	],

}
