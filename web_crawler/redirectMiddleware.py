import os, tempfile, time, sys, logging
import dryscrape
logger = logging.getLogger(__name__)

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class MJRedirectMiddleware(RedirectMiddleware):
    def __init__(self, settings):
        super().__init__(settings)

        # start xvfb to support headless scraping
        if 'linux' in sys.platform:
            dryscrape.start_xvfb()

        self.dryscrape_session = dryscrape.Session(base_url='http://www.amjmed.com/issues')

    def _redirect(self, redirected, request, spider, reason):
        if not self.is_threat_defense_url(redirected.url):
            return super()._redirect(redirected, request, spider, reason)

        logger.debug(f'Zipru threat defense triggered for {request.url}')
        request.cookies = self.bypass_threat_defense(redirected.url)
        request.dont_filter = True
        return request

    def is_threat_defense_url(self, url):
        return '://secure.jbs.elsevierhealth.com/action/getSharedSiteSession?redirect' in url

    def bypass_threat_defense(self, url=None):
        self.wait_for_redirect()
        return self.bypass_threat_defense()

    def wait_for_redirect(self, url=None, wait=0.1, timeout=10):
        url = url or self.dryscrape_session.url()
        for i in range(int(timeout // wait)):
            time.sleep(wait)
            # 如果url发生变化则返回
            if self.dryscrape_session.url() != url:
                return self.dryscrape_session.url()
        logger.error(f'Maybe {self.dryscrape_session.url()} isn\'t a redirect URL?')
        raise Exception('Timed out on the zipru redirect page.')

#https://secure.jbs.elsevierhealth.com/action/getSharedSiteSession?redirect=http%3A%2F%2Fwww.amjmed.com%2Fissues&rc=0&code=ajm-site