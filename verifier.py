import os
from config import *

def init_verify():
	TEST_SRT = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TEST)
	if '.DS_Store' in TEST_SRT:
		TEST_SRT = TEST_SRT[1:]
	TEST_SRT = ['tt'+i.split('_tt')[1].split('.')[0] for i in TEST_SRT]


	TRAIN_SRT = os.listdir(os.getcwd()+'/'+FOLDER_SRT_TRAIN)
	if '.DS_Store' in TRAIN_SRT:
		TRAIN_SRT = TRAIN_SRT[1:]
	TRAIN_SRT = ['tt'+i.split('_tt')[1].split('.')[0] for i in TRAIN_SRT]


	watched_movies = open(FILE_WATCHED_DATA).read().split('\n')
	movies_name = []
	movies_name.extend([(i.split(';')[0],i.split(';')[1]) for i in open(FILE_WATCHLIST_DATA).read().split('\n')])
	movies_name.extend([(w.split(';')[1],w.split(';')[0]) for w in watched_movies])
	movies_name = dict(movies_name)


	WATCHLIST = open(FILE_WATCHLIST_IMDB).read().split('\n')
	WATCHED = open(FILE_WATCHED_IMDB).read().split('\n')
	

	verify_srt(TRAIN_SRT,
				TEST_SRT,
				WATCHLIST,
				WATCHED,
				movies_name)

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
		if srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (dic_movies[srt_imdb_code],srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (dic_movies[srt_imdb_code],srt_imdb_code)

		elif srt_imdb_code in srt_train:
			print '%s/%s/test must to be removed from TEST/database' % (dic_movies[srt_imdb_code],srt_imdb_code) 

	for srt_imdb_code in srt_train:
		
		if srt_imdb_code in new_movies_list and srt_imdb_code in watched_movies_list:
			print '%s/%s was already watched. It was removed from new movie list' % (dic_movies[srt_imdb_code],srt_imdb_code)
			new_movies_list.remove(srt_imdb_code)

		elif srt_imdb_code not in new_movies_list and srt_imdb_code not in watched_movies_list:
			print '%s/%s is not in new movies list and watched movies list' % (dic_movies[srt_imdb_code],srt_imdb_code)



	for imdb_code in new_movies_list:
		if imdb_code not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TEST' % (imdb_code)
			else:
				print '%s/%s srt file must to be Downloaded to TEST' % (dic_movies[imdb_code],imdb_code)

	for code_movie in watched_movies_list:
		if code_movie not in srt_train and code_movie not in srt_test:
			if imdb_code not in dic_movies:
				print '%s srt file must to be Downloaded to TRAIN' % (imdb_code)
			else:
				print '%s/%s srt file must to be Downloaded to TRAIN' % (dic_movies[imdb_code],imdb_code)
		elif code_movie not in srt_train:
			print '%s/%s must to be copied from srt_test to TRAIN' % (dic_movies[imdb_code],imdb_code)

	fnew_movie_titles = open(FILE_WATCHLIST_IMDB,'w')

	for index in xrange(len(new_movies_list)):
		i = new_movies_list[index]
		fnew_movie_titles.write(i)
		if index < len(new_movies_list)-1:
			fnew_movie_titles.write('\n')

	print 'The new_movie_list was updated'

init_verify()



