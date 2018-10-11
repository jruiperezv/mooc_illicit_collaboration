import os
import subprocess
import shutil
import pandas as pd


DATABASE_NAME = "course"


def execute_mysql_query_into_csv(query, file, database_name=DATABASE_NAME, delimiter=","):
    """
    Execute a mysql query into a file.
    :param query: valid mySQL query as string.
    :param file: csv filename to write to.
    :param database_name: name of database to use.
    :param delimiter: type of delimiter to use in file.
    :return: None
    """
    formatted_query = """{} INTO OUTFILE '{}' FIELDS TERMINATED BY '{}' ;""".format(query, file, delimiter)
    command = '''mysql -u root -proot {} -e"{}"'''.format(database_name, formatted_query)
    subprocess.call(command, shell=True)
    return


def load_mysql_dump(dumpfile, database_name=DATABASE_NAME):
    """
    Load a mySQL data dump into DATABASE_NAME.
    :param file: path to mysql database dump
    :return:
    """
    command = '''mysql -u root -proot {} < {}'''.format(database_name, dumpfile)
    subprocess.call(command, shell=True)
    return


def initialize_database(database_name=DATABASE_NAME):
    """
    Start mySQL service and initialize mySQL database with database_name.
    :param database_name: name of database.
    :return: None
    """
    # start mysql server
    subprocess.call("service mysql start", shell=True)
    # create database
    subprocess.call('''mysql -u root -proot -e "CREATE DATABASE {}"'''.format(database_name), shell=True)
    return


def add_course_and_session_columns(csvfile, course, session):
    """
    Add course and session columns to csvfile.
    :param csvfile: path to csv.
    :param course: course name.
    :param session: session.
    :return:
    """
    df = pd.read_csv(csvfile, delimiter=',', quotechar='"', escapechar='\\', error_bad_lines=False, dtype=object)
    df["course"] = course
    df["session"] = session
    df.to_csv(csvfile, index=False)
    return


def extract_coursera_sql_data(course, session, forum_comment_filename="forum_comments.csv",
                              forum_post_filename="forum_posts.csv"):
    """
    Initialize the mySQL database, load files, and execute queries to deposit csv files of data into /input/course/session directory.
    :param course: course name.
    :param session: session id.
    :param forum_comment_filename: name of csv file to write forum comments data to.
    :param forum_post_filename: name of csv file to write forum posts to.
    :return:
    """
    # paths for reading and writing results
    course_session_dir = os.path.join("/input", course, session)
    mysql_default_output_dir = "/var/lib/mysql/{}/".format(
        DATABASE_NAME)  # this is the only location mysql can write to
    forum_comment_fp = os.path.join(course_session_dir, forum_comment_filename)
    forum_post_fp = os.path.join(course_session_dir, forum_post_filename)
    hash_mapping_sql_dump = \
        [x for x in os.listdir(course_session_dir) if "hash_mapping" in x and session in x][0]
    forum_sql_dump = \
        [x for x in os.listdir(course_session_dir) if "anonymized_forum" in x and session in x][0]
    initialize_database()
    load_mysql_dump(os.path.join(course_session_dir, forum_sql_dump))
    load_mysql_dump(os.path.join(course_session_dir, hash_mapping_sql_dump))
    # execute forum comment query and send to csv
    query = """SELECT comment_text FROM forum_comments WHERE is_spam != 1"""
    execute_mysql_query_into_csv(query, file=forum_comment_filename)
    # execute forum post query and send to csv
    query = """SELECT  post_text FROM forum_posts WHERE is_spam != 1"""
    execute_mysql_query_into_csv(query, file=forum_post_filename)
    # move both files to intended location -- this is a hack but it works without needing to chance mysql permissions
    shutil.move(os.path.join(mysql_default_output_dir, forum_comment_filename),
                forum_comment_fp)
    add_course_and_session_columns(forum_comment_fp, course, session)
    shutil.move(os.path.join(mysql_default_output_dir, forum_post_filename),
                forum_post_fp)
    add_course_and_session_columns(forum_post_fp, course, session)
    return