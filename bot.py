#!/usr/bin/python
from urlparse import urljoin
from multiprocessing import Pool

from parsing import getLinks
import db


def start():
	pool = Pool(processes=16)
	queue = []
	websites = db.getJob()
	if websites:
		queue.extend(websites)
	while len(queue):
		print "Browsing", len(queue), 'urls'
		result = pool.map(getLinks, queue)
		print "Adding links"
		newQueue = []
		assert len(queue) == len(result)
		for i in xrange(len(queue)):
			for path in result[i]:
				url = urljoin(queue[i][1], path)
				result = db.addUrl(url, queue[i][0])
				if result:
					newQueue.append(result)
		queue = newQueue
		db.save()
	print "No more job."
	

if __name__ == '__main__':
	db.cleanDatabase()
	start()
