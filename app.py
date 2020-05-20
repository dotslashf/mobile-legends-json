from scrape_hero import ScrapeHero

if __name__ == "__main__":
    sh = ScrapeHero("list_hero.json")
    # sh.initial_download()
    sh.run()
