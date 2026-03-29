from lxml import html
from dataclasses import dataclass
import requests
from datetime import date, datetime

@dataclass
class Solardaten:
    CO2EinsparungGesamt: str = "???"
    EnergieErtragGesamt: str = "???"
    # EnergieErtragJahrChart: str = None

def fetch_solar():

    response = requests.get("https://www.sunnyportal.com/Templates/PublicPage.aspx?page=4985fc6b-b3bb-40d6-9452-1a061cba4d48")
    
    tree = html.fromstring(response.content)

    solardaten = {}

    if (e := tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_PublicPagePlaceholder1_PageUserControl_ctl00_UserControl0_LabelCO2Value"]')):
        solardaten["CO2EinsparungGesamt"] = e[0].text_content().replace(",", "T").replace(".", ",").replace("T", ".")

    if (e := tree.xpath('//*[@id="ctl00_ContentPlaceHolder1_PublicPagePlaceholder1_PageUserControl_ctl00_UserControl0_LabelETotalValue"]')):
        solardaten["EnergieErtragGesamt"] = e[0].text_content().replace(",", "T").replace(".", ",").replace("T", ".")

    # if (e := tree.get_element_by_id('ctl00$ContentPlaceHolder1$PublicPagePlaceholder1$PageUserControl$ctl00$UserControl1$_diagram')):
    #     solardaten["EnergieErtragJahrChart"] = e.get("src")

    # response = requests.get(f"https://www.sunnyportal.com/Templates/PublicChartValues.aspx?ID=5f164c30-715f-4a8c-bb61-ba06a5125ad6&endTime={date.today().strftime("%d.%m.%Y")}%2023:59:59&splang=de-DE&plantTimezoneBias=60&name=")
    # tree = html.fromstring(response.content)

    # tbody = tree.get_element_by_id("ctl00_ContentPlaceHolder1_UserControlChartValues1_Table1").find(".//tbody")

    # data = {}

    # for tr in tbody.findall("tr"):
    #     tds = tr.findall("td")
    #     if len(tds) >= 3:
    #         data[datetime.strptime(tds[0].text_content(), "%H:%M. %d")] = (
    #             tds[1].text_content(),
    #             tds[2].text_content()
    #         )


    return Solardaten(**solardaten)

if __name__ == "__main__":
    print(fetch_solar())