
class ImageDAO:
	@staticmethod
	def testGridFS(form_keys):
		from gridfs import GridFS

		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		fs = GridFS(db)
		gridin = fs.new_file(_id=2, chunk_num=2)
		with client.start_request():
			for i in range(len(form_keys)):
				gridin.write(form_keys[i].encode('UTF-8'))
		client.close()

	@staticmethod
	def storeImagePiece(imgp):
		client = pymongo.MongoClient(MONGODB_URI)
		db = client[DEFAULT_DB]
		
		collection = db['bus_images']
		#img_chunk = base64.b64encode(imgp)
		image = [			
			{'time': datetime.datetime.utcnow(), 'image': img_chunk}
		]		
		
		collection.insert(image)

		client.close()
	
