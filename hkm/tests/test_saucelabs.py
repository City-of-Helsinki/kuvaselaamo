
# -*- coding: utf-8 -*-

import sys
import new
from django.test import LiveServerTestCase
from django.conf import settings
from nose.plugins.attrib import attr
from selenium import webdriver
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.ui import WebDriverWait
from sauceclient import SauceClient

sauce = SauceClient(settings.SAUCELABS_USERNAME, settings.SAUCELABS_ACCESS_KEY)

browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "31"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]


def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator


@on_platforms(browsers)
@attr(slow=1)
@attr(sauce=1)
class SaucelabsTestCase(LiveServerTestCase):
  def setUp(self):
    self.desired_capabilities['name'] = self.id()
    sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"
    self.driver = webdriver.Remote(
      desired_capabilities=self.desired_capabilities,
      command_executor=sauce_url % (settings.SAUCELABS_USERNAME, settings.SAUCELABS_ACCESS_KEY)
    )
    self.driver.implicitly_wait(30)

  def tearDown(self):
    print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
    try:
      if sys.exc_info() == (None, None, None):
          sauce.jobs.update_job(self.driver.session_id, passed=True)
      else:
          sauce.jobs.update_job(self.driver.session_id, passed=False)
    finally:
      self.driver.quit()

  def test_pageload(self):
    self.driver.get(self.live_server_url)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

