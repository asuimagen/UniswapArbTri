import requests
import json
import time
import Triangular_arb_func

""" RETRIEVE GRAPH QL MID PRICES FOR UNISWAP"""
def retrieve_uniswap_information():
    query = """
        query {
          pools(orderBy: totalValueLockedETH,
          orderDirection: desc,
          first: 500) {
            id
            totalValueLockedETH
            feeTier
            token0Price
            token1Price
            token0 { id symbol name decimals }
            token1 { id symbol name decimals }
          }
        }
    """
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    req = requests.post(url, json={'query': query})
    json_dict = json.loads(req.text)
    return json_dict

if __name__ == "__main__":

    while True:
        pairs = retrieve_uniswap_information()["data"]["pools"]
        structure_pairs= Triangular_arb_func.structure_trading_pairs(pairs, limit=500)

        surface_rate_list = []
        for t_pair in structure_pairs:
            surface_rate = Triangular_arb_func.calc_triangular_arb_surface_rate(t_pair, min_rate=0.5)
            if len(surface_rate) > 0:
                surface_rate_list.append(surface_rate)

        # Guardamos lo surface rate de los arbitrajes
        if len(surface_rate_list) > 0:
            with open("option_arbitrage_surface_rate.json", "w") as fp:
                json.dump(surface_rate_list, fp)
                print("File saved.")

        time.sleep(60)
