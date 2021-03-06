# coding=utf-8
import logging
from multiprocessing import Process

import time

from wsgi.db import HumanStorage
from wsgi.properties import force_post_manager_sleep_iteration_time
from wsgi.rr_people.posting.posts import PostsStorage
from wsgi.rr_people.posting.youtube_posts import YoutubeChannelsHandler
from states.processes import ProcessDirector

log = logging.getLogger("posts")

IMPORTANT_POSTS_SUPPLIER_PROCESS_ASPECT = "im_po_su_aspect"


class ImportantYoutubePostSupplier(Process):
    """
    Process which get humans config and retrieve channel_id, after retrieve new posts from it and
    """

    name = "im po su"

    def __init__(self, pq=None, ps=None, ms=None):
        super(ImportantYoutubePostSupplier, self).__init__()

        self.posts_storage = ps or PostsStorage(self.name)
        self.main_storage = ms or HumanStorage(self.name)

        self.posts_supplier = YoutubeChannelsHandler(self.posts_storage)

        self.pd = ProcessDirector("im po su")

        log.info("important post supplier inited")

    def load_new_posts_for_human(self, human_name, channel_id):
        try:
            new_posts = self.posts_supplier.get_new_channel_videos(channel_id)
            new_posts = filter(lambda x: x.for_sub is not None, new_posts)
            log.info("At youtube for [%s] found [%s] new posts:\n%s" % (
                human_name, len(new_posts), ' youtube \n'.join([str(post) for post in new_posts])))

            for post in new_posts:
                self.posts_storage.add_generated_post(post,
                                                      post.for_sub,
                                                      important=True,
                                                      human=human_name,
                                                      video_id=post.video_id
                                                      )

            return len(new_posts), None

        except Exception as e:
            log.error("Exception at im po su: %s; for %s at %s" % (e.message, human_name, channel_id))
            log.exception(e)

    def run(self):
        tracker = self.pd.start_aspect(IMPORTANT_POSTS_SUPPLIER_PROCESS_ASPECT,
                                       tick_time=force_post_manager_sleep_iteration_time / 5,
                                       with_tracking=False)
        if not tracker:
            log.info("Another im po su is worked")
            return

        while True:
            humans_data = self.main_storage.get_humans_info(projection={"user": True, "subs": True, "channel_id": True})
            for human_data in humans_data:
                channel_id = human_data.get("channel_id")
                if channel_id:
                    self.load_new_posts_for_human(human_data.get("user"), channel_id)

            time.sleep(force_post_manager_sleep_iteration_time)


if __name__ == '__main__':
    iyps = ImportantYoutubePostSupplier()
    iyps.start()
