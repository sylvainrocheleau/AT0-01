# scrapy_playwright_ato/logformatter.py
from scrapy.logformatter import LogFormatter
# comment
class ShortItemLogFormatter(LogFormatter):
    def _format_item(self, item):
        # Return a concise representation of the item to avoid giant logs
        try:
            # Convert to dict safely if it is a Scrapy Item
            d = dict(item)
            if "data_dict" in d:
                dd = d.get("data_dict")
                # Summarize data_dict without dumping its content
                if isinstance(dd, dict):
                    # Count top-level keys, list a few, but never dump full odds
                    keys = list(dd.keys())
                    key_count = len(keys)
                    preview_keys = keys[:5]
                    return (
                        f"Item(keys={key_count}, preview_keys={preview_keys}, "
                        f"pipeline_type={d.get('pipeline_type')})"
                    )
                else:
                    return (
                        f"Item(data_dict_type={type(dd).__name__}, "
                        f"pipeline_type={d.get('pipeline_type')})"
                    )
        except Exception:
            pass
        return super()._format_item(item)

    def item_error(self, item, exception, response, spider):
        # Use the parent to create the base log dict, then truncate message body
        d = super().item_error(item, exception, response, spider)
        msg = d.get("message", "")
        # Hard cap message length as a final safety net
        MAX = 1000
        if isinstance(msg, str) and len(msg) > MAX:
            d["message"] = msg[:MAX] + "... [truncated]"
        return d
