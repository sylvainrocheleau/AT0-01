# from itemadapter import ItemAdapter
import os



class ScrapersPipeline:
    # overwrite
    try:
        if os.environ["USER"] == "sylvain":
            f = open("demo_data.txt", "w")
    except:
        pass
    def process_item(self, item, spider):
        # appends
        try:
            if os.environ["USER"] == "sylvain":
                f = open("demo_data.txt", "a")
                # f.write(str(datetime.datetime.utcnow()))
                f.write(str(item))
                f.write( "\n")
                f.close()
        except:
            pass
        return item
