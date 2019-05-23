import argparse
import matplotlib.pyplot as plt
import re
from ProcessData import ProcessData
from GUIManager import GUIManager
from TaskManager import TaskManager
from ReturnStatus import ReturnStatus
from graphviz import Digraph

"""
Code by Lachlan Woods (lsw1@hw.ac.uk)
Files can not be copied and/or distributed without receiving permission from Lachlan Woods

cw2: The DisplayData class contains functions to create histograms and 'also likes' graphs / lists.
"""

class DisplayData:
    """Country codes to continents.
        Adapted from simple_histo.py by Hans-Wolfgang Loidl
        http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/index.html
        """
    country_to_continent = {
        'AF': 'Asia',
        'AX': 'Europe',
        'AL': 'Europe',
        'DZ': 'Africa',
        'AS': 'Oceania',
        'AD': 'Europe',
        'AO': 'Africa',
        'AI': 'North America',
        'AQ': 'Antarctica',
        'AG': 'North America',
        'AR': 'South America',
        'AM': 'Asia',
        'AW': 'North America',
        'AU': 'Oceania',
        'AT': 'Europe',
        'AZ': 'Asia',
        'BS': 'North America',
        'BH': 'Asia',
        'BD': 'Asia',
        'BB': 'North America',
        'BY': 'Europe',
        'BE': 'Europe',
        'BZ': 'North America',
        'BJ': 'Africa',
        'BM': 'North America',
        'BT': 'Asia',
        'BO': 'South America',
        'BQ': 'North America',
        'BA': 'Europe',
        'BW': 'Africa',
        'BV': 'Antarctica',
        'BR': 'South America',
        'IO': 'Asia',
        'VG': 'North America',
        'BN': 'Asia',
        'BG': 'Europe',
        'BF': 'Africa',
        'BI': 'Africa',
        'KH': 'Asia',
        'CM': 'Africa',
        'CA': 'North America',
        'CV': 'Africa',
        'KY': 'North America',
        'CF': 'Africa',
        'TD': 'Africa',
        'CL': 'South America',
        'CN': 'Asia',
        'CX': 'Asia',
        'CC': 'Asia',
        'CO': 'South America',
        'KM': 'Africa',
        'CD': 'Africa',
        'CG': 'Africa',
        'CK': 'Oceania',
        'CR': 'North America',
        'CI': 'Africa',
        'HR': 'Europe',
        'CU': 'North America',
        'CW': 'North America',
        'CY': 'Asia',
        'CZ': 'Europe',
        'DK': 'Europe',
        'DJ': 'Africa',
        'DM': 'North America',
        'DO': 'North America',
        'EC': 'South America',
        'EG': 'Africa',
        'SV': 'North America',
        'GQ': 'Africa',
        'ER': 'Africa',
        'EE': 'Europe',
        'ET': 'Africa',
        'FO': 'Europe',
        'FK': 'South America',
        'FJ': 'Oceania',
        'FI': 'Europe',
        'FR': 'Europe',
        'GF': 'South America',
        'PF': 'Oceania',
        'TF': 'Antarctica',
        'GA': 'Africa',
        'GM': 'Africa',
        'GE': 'Asia',
        'DE': 'Europe',
        'GH': 'Africa',
        'GI': 'Europe',
        'GR': 'Europe',
        'GL': 'North America',
        'GD': 'North America',
        'GP': 'North America',
        'GU': 'Oceania',
        'GT': 'North America',
        'GG': 'Europe',
        'GN': 'Africa',
        'GW': 'Africa',
        'GY': 'South America',
        'HT': 'North America',
        'HM': 'Antarctica',
        'VA': 'Europe',
        'HN': 'North America',
        'HK': 'Asia',
        'HU': 'Europe',
        'IS': 'Europe',
        'IN': 'Asia',
        'ID': 'Asia',
        'IR': 'Asia',
        'IQ': 'Asia',
        'IE': 'Europe',
        'IM': 'Europe',
        'IL': 'Asia',
        'IT': 'Europe',
        'JM': 'North America',
        'JP': 'Asia',
        'JE': 'Europe',
        'JO': 'Asia',
        'KZ': 'Asia',
        'KE': 'Africa',
        'KI': 'Oceania',
        'KP': 'Asia',
        'KR': 'Asia',
        'KW': 'Asia',
        'KG': 'Asia',
        'LA': 'Asia',
        'LV': 'Europe',
        'LB': 'Asia',
        'LS': 'Africa',
        'LR': 'Africa',
        'LY': 'Africa',
        'LI': 'Europe',
        'LT': 'Europe',
        'LU': 'Europe',
        'MO': 'Asia',
        'MK': 'Europe',
        'MG': 'Africa',
        'MW': 'Africa',
        'MY': 'Asia',
        'MV': 'Asia',
        'ML': 'Africa',
        'MT': 'Europe',
        'MH': 'Oceania',
        'MQ': 'North America',
        'MR': 'Africa',
        'MU': 'Africa',
        'YT': 'Africa',
        'MX': 'North America',
        'FM': 'Oceania',
        'MD': 'Europe',
        'MC': 'Europe',
        'MN': 'Asia',
        'ME': 'Europe',
        'MS': 'North America',
        'MA': 'Africa',
        'MZ': 'Africa',
        'MM': 'Asia',
        'NA': 'Africa',
        'NR': 'Oceania',
        'NP': 'Asia',
        'NL': 'Europe',
        'NC': 'Oceania',
        'NZ': 'Oceania',
        'NI': 'North America',
        'NE': 'Africa',
        'NG': 'Africa',
        'NU': 'Oceania',
        'NF': 'Oceania',
        'MP': 'Oceania',
        'NO': 'Europe',
        'OM': 'Asia',
        'PK': 'Asia',
        'PW': 'Oceania',
        'PS': 'Asia',
        'PA': 'North America',
        'PG': 'Oceania',
        'PY': 'South America',
        'PE': 'South America',
        'PH': 'Asia',
        'PN': 'Oceania',
        'PL': 'Europe',
        'PT': 'Europe',
        'PR': 'North America',
        'QA': 'Asia',
        'RE': 'Africa',
        'RO': 'Europe',
        'RU': 'Europe',
        'RW': 'Africa',
        'BL': 'North America',
        'SH': 'Africa',
        'KN': 'North America',
        'LC': 'North America',
        'MF': 'North America',
        'PM': 'North America',
        'VC': 'North America',
        'WS': 'Oceania',
        'SM': 'Europe',
        'ST': 'Africa',
        'SA': 'Asia',
        'SN': 'Africa',
        'RS': 'Europe',
        'SC': 'Africa',
        'SL': 'Africa',
        'SG': 'Asia',
        'SX': 'North America',
        'SK': 'Europe',
        'SI': 'Europe',
        'SB': 'Oceania',
        'SO': 'Africa',
        'ZA': 'Africa',
        'GS': 'Antarctica',
        'SS': 'Africa',
        'ES': 'Europe',
        'LK': 'Asia',
        'SD': 'Africa',
        'SR': 'South America',
        'SJ': 'Europe',
        'SZ': 'Africa',
        'SE': 'Europe',
        'CH': 'Europe',
        'SY': 'Asia',
        'TW': 'Asia',
        'TJ': 'Asia',
        'TZ': 'Africa',
        'TH': 'Asia',
        'TL': 'Asia',
        'TG': 'Africa',
        'TK': 'Oceania',
        'TO': 'Oceania',
        'TT': 'North America',
        'TN': 'Africa',
        'TR': 'Asia',
        'TM': 'Asia',
        'TC': 'North America',
        'TV': 'Oceania',
        'UG': 'Africa',
        'UA': 'Europe',
        'AE': 'Asia',
        'GB': 'Europe',
        'US': 'North America',
        'UM': 'Oceania',
        'VI': 'North America',
        'UY': 'South America',
        'UZ': 'Asia',
        'VU': 'Oceania',
        'VE': 'South America',
        'VN': 'Asia',
        'WF': 'Oceania',
        'EH': 'Africa',
        'YE': 'Asia',
        'ZM': 'Africa',
        'ZW': 'Africa'
    }

    def create_histogram(self, data: ProcessData, input_doc: str, field_name: str, string_function, graph_title: str) -> ReturnStatus:
        """
        Creates a histogram based on the frequency of values in the field_name attribute of the loaded json file,
        for a specific document
        :param data: An instance of the ProcessData class.
        :param input_doc: The id of the document you wish to create a histogram for
        :param field_name: The field name in the json data that you wish to count
        :param string_function: A function to perform over all strings stored in the field_name field of
        the json data (e.g, a function to convert countries to continents)
        :param graph_title: The title of the histogram
        :return: A ReturnStatus code, detailing the result of the function
        """
        assert callable(string_function), "string_function must be a function that operates over a string!"
        display_dict = {}  # a dictionary containing the data to be displayed in a graph

        doc_readers = data.get_document_readers(input_doc)  # gets a list of all users who have read the document
        if not doc_readers:  # if nobody has read the document
            self.log("No readers found. Check your document ID is correct")
            return ReturnStatus.BAD_ID

        for reader in doc_readers: # for all users who read the documents
            read_documents = data.user_id_to_documents.get(reader)  # get all documents read by that user in a list
            relevant_doc = filter(lambda x: True if x["env_doc_id"] == input_doc else False, read_documents)  # select the relevent document from the list
            for doc in relevant_doc:
                if field_name in doc: # check the required json field is in the current doc, otherwise ignore it
                        entry = string_function(doc[field_name])  # apply our string function to the value stored
                        if entry in display_dict:  # count the frequency of each value in the requested field
                            display_dict[entry] += 1
                        else:
                            display_dict[entry] = 1

        if args.verbose:  # if verbose, print statistics to console aswell
            self.log("Statistics for document: " + input_doc)
            for entry in display_dict:
                self.log("%s : %s" % (entry, display_dict[entry]))

        self.display_graph(display_dict, graph_title, input_doc)  # call function to display the histogram
        return ReturnStatus.SUCCESS

    def display_graph(self, display_dict, title: str, doc_id: str):
        """
        Adapted from simple_histo.py by Hans-Wolfgang Loidl http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/index.html
        Takes a dictionary of counts and displays it as a histogram.
        :param display_dict: The dictionary to display as a histogram
        :param title: A string to set as the title of the histogram
        :param doc_id: The id of the document this graph will be generated for
        """
        assert display_dict, "Cannot create a graph from an empty dictionary" # assertion to ensure there is data to display
        n = len(display_dict)
        bar_fun = plt.bar
        bar_ticks = plt.xticks
        bar_label = plt.ylabel
        bar_fun(range(n), list(display_dict.values()), align='center', alpha=0.4)
        bar_ticks(range(n), list(display_dict.keys()))
        bar_label("Views")
        plt.title(title)
        fig = plt.gcf()
        fig.canvas.set_window_title('Document: ' + doc_id)
        plt.show()

    def draw_relation_graph(self, data: ProcessData, also_likes: list, input_doc: str, input_user: str = None) -> ReturnStatus:
        """
        Creates and displays a also likes graph based on a list of also liked documents (from the function also_likes)
        Code adapted from graphvis' documentation. available at https://graphviz.readthedocs.io/en/stable/manual.html
        :param data: A reference to a ProcessData object
        :param also_likes: A list of also liked documents (from the also_likes functions)
        :param input_doc: The ID of the requested document
        :param input_user: The ID of the requested user (optional)
        :return: A ReturnStatus code
        """
        dot = Digraph(strict=True)

        if not also_likes:  # if there are no 'also likes' do not create a graph
            return ReturnStatus.BAD_ID

        dot.node(input_doc[-4:], style="filled", color="green")  # add the input doc to the graph as a green node
        if input_user:  # add the input user to the graph (if specified)
            dot.node(input_user[-4:], style="filled", color="green", shape="rectangle")
            dot.edge(input_user[-4:], input_doc[-4:])  # connect the input reader to input doc

        for doc in also_likes: # for each also liked document
            doc_id = doc[0]  # select the doc id from the tuple of (docID, Readers list)
            dot.node(doc_id[-4:]) # add this doc to the graph (last 4 chars only)
            readers = doc[1]  # select readers from the tuple of (docID, Readers list). This is all readers of the 'also likes' document
            for reader in readers:  # for each reader of the also liked doc
                dot.node(reader[-4:], shape="rectangle")  # add the last 4 digits of the user to the graph
                dot.edge(reader[-4:], doc_id[-4:])  # add an edge from reader to doc
                dot.edge(reader[-4:], input_doc[-4:])  # link each reader to the input doc (since they have all read it)

        dot.render('AlsoLikesGraphs/AlsoLikes.ps', view=True)  # Display the graph
        return ReturnStatus.SUCCESS

    def get_browser_name(self, user_agent: str) -> str:
        """A regular expression to select the main browser name from a user agent string.
        Adapted from regex provided by ticky https://gist.github.com/ticky/3909462
        :param user_agent: a string containing the vistor_useragent details of a single document
        """
        browser_name_regex = "(MSIE|(?!Gecko.+)Firefox|(?!AppleWebKit.+Chrome.+)Safari|(?!AppleWebKit.+)Chrome|AppleWebKit(?!.+Chrome|.+Safari)|Gecko(?!.+Firefox))(?: |\/)(?:[\d\.apre]+)"

        result = re.search(browser_name_regex, user_agent)  # apply the regex to the input string
        if result:
            return result.group(1)  # return a shortened browser name
        else:
            return "Other"  # regex did not match.

    def also_likes(self, data: ProcessData, sorting_function, input_doc: str, input_user:str = None) -> list:
        """
        Returns a list of also likes documents. List elements are a tuple in the form (docID, [readers])
        :param data: A ProcessData instance
        :param sorting_function: A sorting function to order the returned list
        :param input_doc: A document id to find also liked documents for
        :param input_user: A user id to find also liked documents for (Optional)
        :return: An also likes list of tuples in the for (docID, [readers])
        """
        assert callable(sorting_function), "sorting_function must be a function that sorts a dictionary!"
        also_likes_dict = {}

        """If a user id has been specified, check that the user has actually read the requested document.
            If they haven't, give an error message"""
        if input_user != None:
            if input_doc not in data.get_user_read_documents(input_user):
                self.log("The user specified has not read the document with ID: " + input_doc + " Try running without a userID")
                return []

        other_readers = list(filter(lambda x: x != input_user, data.get_document_readers(input_doc)))  # Do not include the input user in the other readers list
        if not other_readers:  # if no body else has read the document
            self.log("No other readers found. Check your document ID is correct")
            return []

        if args.verbose:
            self.log("The readers of document %s are %s" % (input_doc, other_readers))

        # get all documents read by the other users who read the input doc
        for user in other_readers:
            also_read = data.get_user_read_documents(user)  # get a list of other documents that were read by the other users
            for doc in also_read:  # create a dictionary of also liked documents, and the readers of each doc
                if doc != input_doc:  # Do not include the input doc in the also read list
                    if doc in also_likes_dict:
                        also_likes_dict[doc].append(user)
                    else:
                        also_likes_dict[doc] = [user]

        if args.verbose:  # print the also likes dictionary to console if the verbose flag was set
            for doc in also_likes_dict:
                self.log("Document %s was read by %d users: %s" % (doc, len(also_likes_dict[doc]), also_likes_dict[doc]))

        return sorting_function(also_likes_dict)  # return the list sorted by the sorting function

    def log(self, message: str):
        """
        prints a message to console, and the GUI console if it is being shown
        :param message: The string to print
        """
        print(message)
        if args.gui:
            self.gui_manager.append_to_console(message)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--userID", help="The id of the user you wish to display, specified by the field: visitor_uuid")
    parser.add_argument("-d", "--docID", help="The id of the document you wish to display, specified by the field: env_doc_id", required=True)
    parser.add_argument("-t", "--task", help="The task number to run", choices=["2a", "2b", "3a", "3b", "4d", "5"], default="2a")
    parser.add_argument("-f", "--file",help="A file path to a json file containing data from issuu.com", type = str, required=True)
    parser.add_argument("-g", "--gui", help="set this flag to display a gui.", action="store_true")
    parser.add_argument("-v", "--verbose", help="set this flag to display detailed is likes data in the console.", action="store_true")
    args = parser.parse_args()

    data_displayer = DisplayData()  # create an instance of the DisplayData class

    if not args.gui:  # If the gui interface is not used
        task_manager = TaskManager()
        task_manager.run_task(args.task, args.docID, args.userID, args.file, data_displayer)  # run the specified task
    else:  # show the GUI
        gui = GUIManager(args.docID, args.userID, args.file, data_displayer)
        data_displayer.gui_manager = gui  # save the reference to this gui object (needed to print messages)
        gui.display_gui()  # show the gui


