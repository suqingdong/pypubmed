import json


class Article(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return self.__dict__

    def to_json(self, **kwargs):
        return json.dumps(self.__dict__, ensure_ascii=False, **kwargs)

    @property
    def fields(self):
        return list(self.__dict__.keys())

    def __repr__(self):
        return 'Article[{pmid} - {title}]'.format(**self.__dict__)


if __name__ == '__main__':
    
    p = Article(pmid=1, issn='1234-5678', title='test')
    print(p)
    print(p.to_dict())
    print(p.to_json())