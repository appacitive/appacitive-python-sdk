__author__ = 'sathley'


class AppacitiveQuery(object):

    def __init__(self):

        self.page_number = None
        self.page_size = None

        self.order_by = None
        self.is_ascending = None

        self.fields_to_return = []

        self.free_text_tokens = []
        self.language = None

        self.filter = None

    def __repr__(self):
        items = []
        if self.page_number is not None:
            items.append('pNum='+str(self.page_number))

        if self.page_size is not None:
            items.append('pSize='+str(self.page_size))

        if self.order_by is not None:
            items.append('orderBy='+self.order_by)

        if self.is_ascending is not None:
            items.append('isAsc='+self.is_ascending)

        if len(self.fields_to_return)>0:
            items.append('fields='+','.join(self.fields_to_return))

        if len(self.free_text_tokens)>0:
            if self.free_text_language is not None:
                items.append(('language={0}&freetext={1}'.format(self.language, ','.join(self.free_text_tokens))))
            else:
                items.append('freetext='+self.free_text_tokens)

        #   add query dsl for filters
        if self.filter is not None:
            items.append('filter='+self.filter)

        return '&'.join(items)