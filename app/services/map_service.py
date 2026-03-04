import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CrawlResult, LLMConfig, LLMExtractionStrategy
from pydantic import BaseModel, Field
from app.models.map import Link, LinkNode, MapResult, Node, SummaryModel
from os import getenv


class MapService:

    __extraction_prompt = """Get the main call to action of the page if any, or the summary of the page in less than 10 words"""

    __extra_llm_args = {
        "temperature": 0,
        "top_p": 0.9,
        "max_tokens": 200000
    }

    __llm_config = LLMConfig(
        provider="gemini/gemini-2.0-flash-lite",
        api_token=getenv("API_KEY")
    )

    __extraction_strategy = LLMExtractionStrategy(
        llm_config=__llm_config,
        schema=SummaryModel.model_json_schema(),
        extraction_type="schema",
        instruction=__extraction_prompt,
        extra_args=__extra_llm_args,
    )

    __crawler_run_config = CrawlerRunConfig(
        exclude_all_images=True,
        exclude_external_links=True,
        extraction_strategy=__extraction_strategy
    )

    def __get_pages_from_links(self, links: list[Link]) -> list[str]:
        return list({link['href']
                     .split('?')[0]
                     .split('#')[0] for link in links
                     })

    def __get_summary_from_result(self, result: CrawlResult) -> str:
        if result.extracted_content:
            if len(json.loads(result.extracted_content)) > 0 and 'summary' in json.loads(result.extracted_content)[0]:
                return json.loads(result.extracted_content)[0]['summary']
        return "couldn't extract summary"

    def __extract_global_links(self, mentioned_dict: dict[str, int]) -> list[str]:
        total_links = len(mentioned_dict)
        global_links = [
            url for url, count in mentioned_dict.items() if count > total_links * 0.8]
        return global_links

    async def map_website(self, start_url: str, max_depth: int = 3) -> MapResult:
        """Map a website starting from the given URL"""
        graph: dict[str, Node] = dict()
        mentionedCount = {start_url: 1}

        scrape_queue: list[LinkNode] = [
            LinkNode(url=start_url, depth=0)]

        while scrape_queue and scrape_queue[0].depth < max_depth:
            current_url = scrape_queue.pop(0)
            print(f"Processing: {current_url}")

            async with AsyncWebCrawler(verbose=True) as crawler:
                result: CrawlResult = await crawler.arun(
                    config=self.__crawler_run_config,
                    url=current_url.url,
                )  # type: ignore

                assert result is not None, "Crawler did not return any results"

                internal_links: list[Link] = result.links.get(
                    'internal', [])  # type: ignore

                unique_links = self.__get_pages_from_links(internal_links)
                summary = self.__get_summary_from_result(result)

                graph[current_url.url] = Node(
                    url=current_url.url, title=summary)
                print("summary" + summary)

                unvisisted_links = [
                    link for link in unique_links if link not in mentionedCount]
                graph[current_url.url].children = unvisisted_links
                unvisited_dict_entry = {link: 1 for link in unvisisted_links}
                mentionedCount.update(unvisited_dict_entry)

                unvisited_link_nodes = [LinkNode(
                    url=link, depth=current_url.depth + 1) for link in unvisisted_links]

                scrape_queue.extend(unvisited_link_nodes)

                visited_links = [
                    link for link in unique_links if link in mentionedCount]
                visited_dict_entry = {
                    link: mentionedCount[link] + 1 for link in visited_links}
                mentionedCount.update(visited_dict_entry)

        global_links = self.__extract_global_links(mentionedCount)

        return MapResult(start_url=start_url, global_links=global_links, nodes=graph)
