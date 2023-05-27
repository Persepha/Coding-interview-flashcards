from common.services import CRUDBase
from flashcards.models.topic import Topic
from flashcards.schemas.topic_schemas import TopicCreateModel, TopicUpdateModel


class CRUDTopic(CRUDBase[Topic, TopicCreateModel, TopicUpdateModel]):
    pass


topic_crud = CRUDTopic(Topic)
