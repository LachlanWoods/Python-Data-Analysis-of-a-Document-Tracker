import json
from ReturnStatus import ReturnStatus

"""
Code by Lachlan Woods (lsw1@hw.ac.uk)
Files can not be copied and/or distributed without receiving permission from Lachlan Woods

ProcessData: Reads in a JSON file line by line, and builds a dictionary of userID -> read documents (in json format)
and a dictionary of documentID -> userIDs of the document's readers
"""

class ProcessData:

    def __init__(self):
        self.user_id_to_documents = {}  # create an empty dictionary to store userID -> document read entries
        self.doc_id_to_readers = {}  # create an empty dictionary to store docID -> a list of reader IDs

    def load_json(self, file_path: str, filter_function, display) -> ReturnStatus:
        """
        Reads a json file line by line and populates the user_id_to_documents and doc_id_to_readers dictionaries
        :param file_path: The file path of the json to read
        :param filter_function: A function to filter the json entries to be saved (for performance reasons)
        :param display: A DisplayData object (needed to print errors to gui console)
        :return: A ReturnStatus indicating if the file was loaded successfully or not
        """
        assert callable(filter_function), "filter_function must be a function that filters json objects!"

        line_num = 0  # The current line we are reading from (for better error messages)
        try:
            with open(file_path, 'r') as f:
                for line in f:  # read the json file line by line
                    line_num = line_num + 1  # track the line number we are currently reading from
                    data = json.loads(line)  # load the current line
                    if data["event_type"] == "read":  # check the json entry is a read event
                        if filter_function(data):  # only save entries to our dictionaries that pass the filterFunction
                            self.add_read_document(data["visitor_uuid"], data)
                            self.add_doc_reader(data["env_doc_id"], data["visitor_uuid"])
            f.close()  # close the json file after reading all lines
            return ReturnStatus.SUCCESS
        except IOError as e:  # catch IO exceptions
            display.log("Unable to load file " + file_path + " Reason: " + str(e) + ". Error occurred on line " + str(line_num) + " of " + file_path)
            return ReturnStatus.BAD_File
        except Exception as e:  # catch all other exceptions
            display.log("An error occurred while reading " + file_path + ". Reason: " + str(e) + ". Error occurred on line " + str(line_num) + " of " + file_path)
            return ReturnStatus.BAD_File

    def add_read_document(self, reader_id: str, doc_object):
        """
        Adds a document to the list of a user's read documents
        :param reader_id: The ID of the user
        :param doc_object: A json object for the read event
        """
        if reader_id in self.user_id_to_documents: # The user is already a key in our dictionary
            self.user_id_to_documents[reader_id].append(doc_object)
        else: # add the user as a key
            self.user_id_to_documents[reader_id] = [doc_object]

    def add_doc_reader(self, doc_id: str, reader_id: str):
        """
        Add a user to the list of readers of a document
        :param doc_id: The ID of the document
        :param reader_id: The ID of the reader
        """
        if doc_id in self.doc_id_to_readers:
            if reader_id not in self.doc_id_to_readers[doc_id]: # do not add duplicate entries
                self.doc_id_to_readers[doc_id].append(reader_id)
        else:
            self.doc_id_to_readers[doc_id] = [reader_id]

    def get_document_readers(self, doc_id: str) -> list:
        """
        Returns a list of all users who have read a document
        :param doc_id: The document to return the readers for
        :return: A list of user IDs for the people who have read a document
        """
        if self.doc_id_to_readers.get(doc_id) == None: # if there are no readers of a document
            return []
        else:
            return self.doc_id_to_readers.get(doc_id)

    def get_user_read_documents(self, user_id: str) -> list:
        """
        Returns a list of IDs for the documents that have been read by a user
        :param user_id: The ID of the user
        :return: A list of Document IDs read by user_id
        """
        #task 4b. uses list comprehension
        user_read_list = self.user_id_to_documents.get(user_id) #a list of documents read by this user in json format
        if user_read_list == None:
            return []
        else:
            # use list comprehension to only return the document id. A set is used to remove duplicate entries
            user_read_ids = set([d["env_doc_id"] for d in user_read_list])
            return list(user_read_ids)



