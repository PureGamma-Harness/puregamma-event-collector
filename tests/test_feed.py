import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from main import parse_feed


class FeedTests(unittest.TestCase):
    def test_rdf_reads_namespaced_item_fields(self):
        raw = b'''<rdf:RDF
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns="http://purl.org/rss/1.0/"
            xmlns:dc="http://purl.org/dc/elements/1.1/">
          <channel rdf:about="https://example.com/feed"><title>Feed</title></channel>
          <item rdf:about="https://example.com/news">
            <title>News &amp; updates</title>
            <link>https://example.com/news</link>
            <description>&lt;p&gt;Full story&lt;/p&gt;</description>
            <dc:date>2026-10-28T12:00:00Z</dc:date>
          </item>
        </rdf:RDF>'''
        self.assertEqual(parse_feed(raw), [{
            "title": "News & updates", "link": "https://example.com/news",
            "guid": "", "summary": "Full story", "published": 1793188800,
        }])

    def test_rss_two_keeps_unnamespaced_fields(self):
        raw = b'''<rss version="2.0"><channel><item>
          <title>RSS headline</title><link>https://example.com/rss</link>
          <guid>rss-1</guid><description>RSS body</description>
          <pubDate>Wed, 28 Oct 2026 12:00:00 GMT</pubDate>
        </item></channel></rss>'''
        self.assertEqual(parse_feed(raw), [{
            "title": "RSS headline", "link": "https://example.com/rss",
            "guid": "rss-1", "summary": "RSS body", "published": 1793188800,
        }])

    def test_atom_keeps_namespaced_fields(self):
        raw = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <title>Atom headline</title><id>atom-1</id><summary>Atom body</summary>
          <link rel="self" href="https://example.com/feed"/>
          <link href="https://example.com/atom"/>
          <updated>2026-10-28T12:00:00Z</updated>
        </entry></feed>'''
        self.assertEqual(parse_feed(raw), [{
            "title": "Atom headline", "link": "https://example.com/atom",
            "guid": "atom-1", "summary": "Atom body", "published": 1793188800,
        }])


if __name__ == "__main__":
    unittest.main()
