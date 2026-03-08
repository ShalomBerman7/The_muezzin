from get_metadata import GetMetadata
from publisher import Publisher
import os

# PATH = r'C:\github\The_muezzin\podcasts'
PATH = os.getenv('PODCASTS_PATH', '/app/podcasts')
TOPIC = 'metadata'

if __name__ == '__main__':

    c = GetMetadata(PATH)
    data = c.get_metadata()

    publisher = Publisher(TOPIC, data)
    publisher.publish()
