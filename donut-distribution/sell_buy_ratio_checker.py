from typing import Dict, List, Tuple, Set

ORIGIN_WALLET = "0x439cee4cc4ecbd75dc08d9a17e92bddcc11cdb8c"               
LP_ADDRESS = "0x65f7a98d87bc21a3748545047632fef4d3ff9a67"
REWARD_ADDRESS = "0x3ef3d8ba38ebe18db133cec108f4d14ce00dd9ae"
CHECKED_ADDRESS = "0x5ed61dee19b3355cf125a5cb95bec8f344523628"
GNOSIS_SHUTTLE = "0x51871f5fb2e8a04a874f02262b5bef28c60ac6ee"

def get_address_transfers() -> Dict[str, List[float]]:
    transfers: Dict[str, List[float]] = {}
    transfers["tokens_received_from_origin"] = [0, 0]
    transfers["Sold"] = [0, 0]
    transfers["tokens_sent_to_lp"] = [0, 0]
    transfers["tokens_received_from_lp"] = [0, 0]
    transfers["rewards_received_from_lp"] = [0, 0]
    transfers["gnosis_shuttle"] = [0, 0]
    local_path = 'D:\\Scripts\\RedditAPIScript\\donut-distribution\\input\\transfer\\tokentxns-donut.csv'
    with open(local_path) as f:
        lines = f.readlines()
        for line in lines:
            data = line.split('","')[3:8]
            amount = data[3]
            if "," in amount:
                amount = amount.replace(",","")
            if data[1].lower() == ORIGIN_WALLET:
                transfers["tokens_received_from_origin"][0] += float(amount)
                transfers["tokens_received_from_origin"][1] += float(data[4][1:])
            if data[1].lower() == CHECKED_ADDRESS:
                if data[2].lower() != LP_ADDRESS:
                    transfers["Sold"][0] += float(amount)
                    transfers["Sold"][1] += float(data[4][1:])
                else:
                    transfers["tokens_sent_to_lp"][0] += float(amount)
                    transfers["tokens_sent_to_lp"][1] += float(data[4][1:])
            if data[1].lower() == LP_ADDRESS:
                transfers["tokens_received_from_lp"][0] += float(amount)
                transfers["tokens_received_from_lp"][1] += float(data[4][1:])                
            if data[1].lower() == REWARD_ADDRESS:
                transfers["rewards_received_from_lp"][0] += float(amount)
                transfers["rewards_received_from_lp"][1] += float(data[4][1:])
            if data[1].lower() == GNOSIS_SHUTTLE:
                transfers["gnosis_shuttle"][0] += float(amount)
                transfers["gnosis_shuttle"][1] += float(data[4][1:])
    return transfers




if __name__ == "__main__":
    transfers = get_address_transfers()

    membership = 0
    current_balance = 171024.0651
    earned = transfers['tokens_received_from_origin'][0]
    net_lp = transfers['tokens_sent_to_lp'][0] - transfers["tokens_received_from_lp"][0]

    positive_values = current_balance + net_lp + membership
    if earned > 0:
        ratio = 100 * (1 - positive_values / earned)
    print(ratio)
    ratio_difference = positive_values - 0.75 * earned
    print(ratio_difference)
    gnosis = transfers['gnosis_shuttle'][0]
    ratio_difference = positive_values - 0.75 * (earned + gnosis)
    print(ratio_difference)
