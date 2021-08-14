import threading
from selenium import webdriver
import unittest
from app import create_app, fake, db
from app.models import Role, User
import re

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        #start chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless') 
        try:
            cls.client = webdriver.Chrome(chrome_options=options)
        except:
            pass

        #skip these tests if the browser could not be started
        if cls.client:
            #create application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            #suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            #create database and populate with fake data
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            #add an administrator user
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='john@example.com', username='john', password='cat', role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            #start Flask server in a thread
            cls.server_thread = threading.Thread(
                target=cls.app.run, kwargs={
                    'debug': 'false',
                    'use_reloader': 'false',
                    'use_debugger': 'false'
                }
            )
            cls.server_thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client:
            #stop Flask server amd browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.quit()
            cls.server_thread.join()

            #destroy database
            db.drop_all()
            db.session.remove()

            #remove the app context
            cls.app_context.pop()

    def setUp(self) -> None:
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self) -> None:
        pass


    def test_admin_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        #navigate to login page
        self.client.find_element_by_link_text('Log in').click()
        self.assertIn('<h1>Log in</h1>', self.client.page_source)
        
        #log in
        self.client.find_element_by_name('email').send_keys('john@example.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('Hello,\s+john!', self.client.page_source))

        #navigate to user profile
        self.client.find_element_by_link_text('Profile').click()
        self.assertIn('<h1>john</h1>', self.client.page_source)