from scrape_hero import ScrapeHero

if __name__ == "__main__":
    sh = ScrapeHero()
    sh.download_list_heroes()
    # sh.initial_download()
    sh.run()
