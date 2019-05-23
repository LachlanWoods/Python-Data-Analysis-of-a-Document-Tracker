from ProcessData import ProcessData
from ReturnStatus import ReturnStatus

"""
Code by Lachlan Woods (lsw1@hw.ac.uk)
Files can not be copied and/or distributed without receiving permission from Lachlan Woods

TaskManager: Takes input from the user (terminal or GUI) and calls functions based on the specified task number.
Also contains my implementation of a sorting function for tasks 4 and 5
"""

class TaskManager:

    def run_task(self, task: str, input_doc: str, input_user: str, file: str, display) -> ReturnStatus:
        """
        Runs a specific task using the user input provided
        :param task: The task ID to run
        :param input_doc: The document ID to run the task for
        :param input_user: The user ID to run the task for
        :param file: The file path of the json data to analysed
        :param display: A DisplayData instance
        :return: A ReturnStatus code specifying the result of the task
        """
        if not input_doc:
            display.log("Missing document ID. A document ID is needed to perform all tasks")
            return ReturnStatus.BAD_ID
        else:
            data = ProcessData()  # create a new ProcessData object
            if task == "2a":
                data_filter = lambda x: True if input_doc == x["env_doc_id"] else False # only save read events for the requested doc
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    result = display.create_histogram(data, input_doc, "visitor_country", lambda x: x, "Views by Country")
                    return result
            elif task == "2b":
                data_filter = lambda x: True if input_doc == x["env_doc_id"] else False # only save read events for the requested doc
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    result = display.create_histogram(data, input_doc, "visitor_country", lambda x: display.country_to_continent[x],"Views by Continent")
                    return result
            elif task == "3a":
                data_filter = lambda x: True if input_doc == x["env_doc_id"] else False # only save read events for the requested doc
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    result = display.create_histogram(data, input_doc, "visitor_useragent", lambda x: x, "Views by Browser")
                    return result
            elif task == "3b":
                data_filter = lambda x: True if input_doc == x["env_doc_id"] else False # only save read events for the requested doc
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    result = display.create_histogram(data, input_doc, "visitor_useragent", display.get_browser_name, "Views by Browser")
                    return result
            elif task == "4d":
                data_filter = lambda x: x  # load all read events (we might need them for also likes lists)
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    likes_list = display.also_likes(data, self.my_sorting_function, input_doc, input_user)
                    if likes_list:
                        display.log("\nAlso likes list for doc %s:" %input_doc)
                        for also_liked in likes_list:
                            display.log(" - Doc %s was liked by %d other readers" % (also_liked[0], len(also_liked[1])))
                        display.log("\n")
                        return ReturnStatus.SUCCESS
                    else:
                        return ReturnStatus.NO_LIKES
            elif task == "5":
                data_filter = lambda x: x # load all read events (we might need them for also likes lists)
                load_result = data.load_json(file, data_filter, display)
                if load_result == ReturnStatus.BAD_File:
                    return load_result
                else:
                    likes_list = display.also_likes(data, self.my_sorting_function, input_doc, input_user)
                    result = display.draw_relation_graph(data, likes_list, input_doc, input_user)
                    return result
            else:
                print("Unknown task id. valid options are [2a, 2b, 3a, 3b, 4d, 5]");
                return ReturnStatus.Bad_Task

    def my_sorting_function(self, likes: dict) -> list:
        """
        My sorting function for task 4 and 5. Sorts a list by most read
        :param likes: The dictionary of doc_id to a list of readers
        :return: A sorted also_likes list
        """
        ordered_list = []
        for k in sorted(likes, key=lambda k: len(likes[k]), reverse=True):  # sort likes_list by number of readers
            ordered_list.append((k, likes[k]))  # create a list of ordered (doc, readers) tuples
        return ordered_list[:10]  # return top 10 most popular documents
