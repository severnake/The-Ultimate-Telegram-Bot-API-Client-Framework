import json
import six

""" Telegram Available methods
    All methods in the Bot API are case-insensitive. We support GET and POST HTTP methods. 
    Use either URL query string or application/json or application/x-www-form-urlencoded or multipart/form-data for passing parameters in Bot API requests.
    On successful call, a JSON-object containing the result will be returned.
"""


class Dictionaryable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to dictionary,
    All subclasses of this class must override to_dic.
    """

    def to_dic(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class JsonDeserializable(object):
    """
    Subclasses of this class are guaranteed to be able to be created from a json-style dict or json formatted string,
    All subclasses of this class must override de_json.
    """

    @classmethod
    def de_json(cls, json_type):
        """
        Returns an instance of this class from the given json dict or string.

        This function must be overridden by subclasses.
        :return: an instance of this class created from the given json dict or string.
        """
        raise NotImplementedError

    @staticmethod
    def check_json(json_type):
        """
        Checks whether json_type is a dict or a string. If it is already a dict, it is returned as-is,
        If it is not, it is converted to a dict by means of json.loads(json_type),
        :param json_type:
        :return:
        """
        try:
            str_types = (str, unicode)
        except NameError:
            str_types = (str,)

        if type(json_type) == dict:
            return json_type
        elif type(json_type) in str_types:
            return json.loads(json_type)
        else:
            raise ValueError("json_type should be a json dict or string.")

    def __str__(self):
        d = {}
        for x, y in six.iteritems(self.__dict__):
            if hasattr(y, '__dict__'):
                d[x] = y.__dict__
            else:
                d[x] = y

        return six.text_type(d)


class JsonSerializable(object):
    """
    Subclasses of this class are guaranteed to be able to be converted to JSON format,
    All subclasses of this class must override to_json.
    """

    def to_json(self):
        """
        Returns a JSON string representation of this class.

        This function must be overridden by subclasses.
        :return: a JSON formatted string.
        """
        raise NotImplementedError


class Animation(JsonDeserializable):
    """ This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) 
        :param file_id: [STRING] Identifier for this file, which can be used to download or reuse the file.
        :param file_unique_id: [STRING] Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file..
        :param width: [INTEGER] Video width as defined by sender.
        :param height: [INTEGER] Video height as defined by sender.
        :param duration: [INTEGER] Duration of the video in seconds as defined by sender.
        :param thumb: [PhotoSize] Optional. Animation thumbnail as defined by sender.
        :param file_name: [STRING] Optional. Original animation filename as defined by sender.
        :param mime_type: [STRING] Optional. MIME type of the file as defined by sender.
        :param file_size: [INTEGER] Optional. File size.
        :return JSON_OBJECT:
    """

    def __init__(self, file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size

    @classmethod
    def de_json(cls, json_string):
        obj = cls.check_json(json_string)
        file_id = obj['file_id']
        file_unique_id = obj['file_unique_id']
        width = obj['width']
        height = obj['height']
        duration = obj['duration']
        thumb = None
        if 'thumb' in obj:
            thumb = PhotoSize.de_json(obj['thumb'])
        file_name = None
        if 'file_name' in obj:
            file_name = obj.get('file_name')
        mime_type = None
        if 'mime_type' in obj:
            mime_type = obj.get('mime_type')
        file_size = None
        if 'file_size' in obj:
            file_size = obj.get('file_size')
        return cls(file_id, file_unique_id, width, height, duration, thumb, file_name, mime_type, file_size)
