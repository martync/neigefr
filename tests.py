from django.test import TestCase
from neigefr.flake import parse_body, process
from neigefr.models import Snowflake


class FlakeTest(TestCase):

    def test_parse_body(self):
        content = "#neigefr 64100 2/10"
        flake = parse_body(content)
        self.assertEquals(flake.zipcode, '64100')
        self.assertEquals(flake.ranking, 2)

    def test_process(self):
        data = {
            "iso_language_code": "fr",
            "to_user_name": "Seb Solere",
            "to_user_id_str": "137994749",
            "profile_image_url_https": "https://si0.twimg.com/profile_images/329883768/3697028883_0ae17360f9_b_normal.jpg",
            "from_user_id_str": "14979950",
            "text": "#neigefr 64100 2/10",
            "from_user_name": "Bruno Bord",
            "in_reply_to_status_id_str": "165073316988723201",
            "profile_image_url": "http://a3.twimg.com/profile_images/329883768/3697028883_0ae17360f9_b_normal.jpg",
            "id": 165074248593969152,
            "to_user": "sebsolere",
            "source": "&lt;a href=&quot;http://twirssi.com&quot; rel=&quot;nofollow&quot;&gt;Twirssi&lt;/a&gt;",
            "in_reply_to_status_id": 165073316988723201,
            "id_str": "165074248593969152",
            "from_user": "brunobord",
            "from_user_id": 14979950,
            "to_user_id": 137994749,
            "geo": None,
            "created_at": "Thu, 02 Feb 2012 14:09:02 +0000",
            "metadata": {
                "result_type": "recent"
            }
        }
        snowflake = process(data)
        zipcode = snowflake.zipcode
        self.assertEquals(zipcode.zipcode, '64100')
        self.assertEquals(zipcode.city, 'Bayonne')
        self.assertEquals(zipcode.latitude, '43.5031621')
        self.assertEquals(zipcode.longitude, '-1.4724751')
        self.assertEquals(snowflake.tweet_id, 165074248593969152L)
        self.assertEquals(snowflake.latitude, zipcode.latitude)
        self.assertEquals(snowflake.longitude, zipcode.longitude)
        self.assertEquals(snowflake.rank, 2)

    def test_flakesize(self):
        snowflake = Snowflake()
        snowflake.rank = 0
        self.assertEquals(snowflake.flakesize, 0)
        snowflake.rank = 1
        self.assertEquals(snowflake.flakesize, 6)
        snowflake.rank = 2
        self.assertEquals(snowflake.flakesize, 8)
        snowflake.rank = 3
        self.assertEquals(snowflake.flakesize, 8)
        snowflake.rank = 4
        self.assertEquals(snowflake.flakesize, 12)
        snowflake.rank = 5
        self.assertEquals(snowflake.flakesize, 16)
        snowflake.rank = 6
        self.assertEquals(snowflake.flakesize, 16)
        snowflake.rank = 7
        self.assertEquals(snowflake.flakesize, 24)
        snowflake.rank = 8
        self.assertEquals(snowflake.flakesize, 24)
        snowflake.rank = 9
        self.assertEquals(snowflake.flakesize, 32)
        snowflake.rank = 10
        self.assertEquals(snowflake.flakesize, 32)

        # special cases
        snowflake.rank = None
        self.assertEquals(snowflake.flakesize, 8)
        snowflake.rank = 11
        self.assertEquals(snowflake.flakesize, 32)
