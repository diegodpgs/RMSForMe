import os
import nltk
from environment import *

def init_verify():

	watched_data = open(FILE_WATCHED_DATA).read().split('\n')
	watched_imdb = open(FILE_WATCHED_IMDB).read().split('\n')
	watchlist_imdb = open(FILE_WATCHLIST_IMDB).read().split('\n')
	watchlist_data = open(FILE_WATCHLIST_DATA).read().split('\n')
	
	movies_name = []
	movies_name.extend([(i.split(';')[0],[i.split(';')[1],int(i.split(';')[2])]) for i in watchlist_data])
	
	movies_name.extend([(i.split(';')[0],[i.split(';')[1],int(i.split(';')[2])]) for i in watched_data])
	movies_name = dict(movies_name)

	#****---------------    SRT   ---------------****#
	test_srt = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TEST)
	if '.DS_Store' in test_srt:
		test_srt = test_srt[1:]
	test_srt = ['tt'+i.split('_tt')[1].split('.')[0] for i in test_srt]


	train_srt = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TRAIN)
	if '.DS_Store' in train_srt:
		train_srt = train_srt[1:]
	train_srt = ['tt'+i.split('_tt')[1].split('.')[0] for i in train_srt]

	#****---------------    TAG   ---------------****#
	test_tag = os.listdir(os.getcwd()+'/'+FOLDER_TAG_TEST)
	if '.DS_Store' in test_tag:
		test_tag = test_tag[1:]
	test_tag = ['tt'+i.split('_tt')[1].split('.')[0] for i in test_tag]


	train_tag = os.listdir(os.getcwd()+'/'+FOLDER_TAG_TRAIN)
	if '.DS_Store' in train_tag:
		train_tag = train_tag[1:]
	train_tag = ['tt'+i.split('_tt')[1].split('.')[0] for i in train_tag]

	verify_movies_data(watched_imdb,watchlist_imdb,watched_data,watchlist_data)
	verify_srt(train_srt,test_srt,watchlist_imdb,watched_imdb,movies_name)
	verify_tag(train_tag,test_tag,watchlist_imdb,watched_imdb,movies_name)
	#verify_utterance()

def verify_srt(srt_train,srt_test,new_movies_list,watched_movies_list,dic_movies):
	
	"""
		srt_train,srt_test,watched_movies_list,new_movies:  [list of IMDB code]
		dic_movies: a dicionary that maps IMDB_code to movie title

		What will be virified?
			srt_train
			srt_test

		Verify if
		- there are srt file duplicated in test and train
		- a file labeled as test was not watched yet
		- a file labeled as train was already watched
		- there are srt file to download

	"""

	for srt_imdb_code in srt_test:

		if srt_imdb_code not in dic_movies:
			print '%s is not within watchlist.imdb and not in watched.imdb, but in srt/test' % srt_imdb_code
			continue
		movie_title = dic_movies[srt_imdb_code][0]

		if not (1930<= dic_movies[srt_imdb_code][1] <= 2015):
			print '%s is not considered for srt because it was released on %d' % (movie_title,dic_movies[srt_imdb_code][1])

		elif srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (movie_title,srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (movie_title,srt_imdb_code)

		elif srt_imdb_code in srt_train:
			print '%s/%s/test must to be removed from TEST/database' % (movie_title,srt_imdb_code) 

	for srt_imdb_code in srt_train:

		if srt_imdb_code not in dic_movies:
			print '%s is not within watchlist.imdb and not in watched.imdb, but in srt/train' % srt_imdb_code
			continue
		
		if srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (dic_movies[srt_imdb_code][0],srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (dic_movies[srt_imdb_code][0],srt_imdb_code)


	

	for imdb_code in new_movies_list:

		if imdb_code not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TEST' % (imdb_code)
			else:
				if not (1930<= dic_movies[imdb_code][1] <= 2015):
					print '%s is not considered for srt because it was released on %d' % (dic_movies[imdb_code][0],dic_movies[imdb_code][1])
					continue

				else:
					print '%s/%s srt file must to be Downloaded to TEST' % (dic_movies[imdb_code][0],imdb_code)

	for imdb_code in watched_movies_list:
		if imdb_code not in srt_train and imdb_code not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TRAIN' % (imdb_code)
			else:
				print '%s/%s srt file must to be Downloaded to TRAIN' % (dic_movies[imdb_code][0],imdb_code)
		elif imdb_code not in srt_train:
			print '%s/%s must to be copied from srt_test to TRAIN' % (dic_movies[imdb_code][0],imdb_code)

	fnew_movie_titles = open(FILE_WATCHLIST_IMDB,'w')

	for index in xrange(len(new_movies_list)):
		i = new_movies_list[index]
		fnew_movie_titles.write(i)
		if index < len(new_movies_list)-1:
			fnew_movie_titles.write('\n')

	print 'The new_movie_list was updated'

def verify_movies_data(watched_imdb,watchlist_imdb,watched_data,watchlist_data):
	"""
		What will be verified?
			watchlist.data
			watchlist.imdb
			watched.data
			watched.imdb
	"""

	if len(watchlist_imdb) != len(set(watchlist_imdb)):
		print 'There are register duplicated in watchlist.imdb'
		f = nltk.FreqDist(watchlist_imdb)
		for i in f.most_common(50):
			if i[1] > 1:
				print '----',i[0], 'was duplicated',i[1],'times in watchlist.imdb'

	if len(watched_imdb) != len(set(watched_imdb)):
		print 'There are register duplicated in watched.imdb'
		f = nltk.FreqDist(watched_imdb)
		for i in f.most_common(50):
			if i[1] > 1:
				print '----',i[0], 'was duplicated',i[1],'times in watched.imdb'
		

	if len(watchlist_data) != len(set(watchlist_data)):
		print 'There are register duplicated in watchlist.data'
		f = nltk.FreqDist(watchlist_data)
		for i in f.most_common(50):
			if i[1] > 1:
				print '----',i[0], 'was duplicated',i[1],'times'

	if len(watched_data) != len(set(watched_data)):
		print 'There are register duplicated in watched.data'
		f = nltk.FreqDist(watched_data)
		for i in f.most_common(50):
			if i[1] > 1:
				print '----',i[0], 'was duplicated',i[1],'times'


	if len(watchlist_data) != len(watchlist_imdb):
		watchlist_data_imdb_code = [i.split(';')[0] for i in watchlist_data]
		for imdb_code in watchlist_imdb:
			if imdb_code not in watchlist_data_imdb_code:
				print '%s is within watchlist_imdb, but not in watchlist_data' % imdb_code

	if len(watched_data) != len(watched_imdb):
		watched_data_imdb_code = [i.split(';')[0] for i in watched_data]
		for imdb_code in watched_imdb:
			if imdb_code not in watched_data_imdb_code:
				print '%s is within watched_imdb, but not in watched_data' % imdb_code

def verify_tag(tag_train,tag_test,new_movies_list,watched_movies_list,dic_movies):


	for imdb_code in tag_test:
		if imdb_code not in new_movies_list and imdb_code in watched_movies_list:
			print 'Move %s/%s from test to TAG_train_folder' % (imdb_code,dic_movies[imdb_code][0])

	for imdb_code in new_movies_list:
		if imdb_code not in tag_test and imdb_code not in watched_movies_list:
			print 'Download %s and move to TAG_TEST folder' % (imdb_code)

	for imdb_code in watched_movies_list:
		if imdb_code not in tag_train and imdb_code not in new_movies_list:
			print 'Download %s and move to TAG_TRAIN folder' % (imdb_code)

def verify_utterance():
	raise Exception()

init_verify()



