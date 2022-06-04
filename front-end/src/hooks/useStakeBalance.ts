import networkMapping from "../chain-info/deployments/map.json";
import tokenFarm from "../chain-info/contracts/TokenFarm.json";
import { BigNumber, utils } from "ethers";
import { Contract } from "@ethersproject/contracts";
import { useEthers } from "@usedapp/core";
import { useCall } from "@usedapp/core";

// custom hook to get staked balance for a given token
export const useStakeBalance = (
  tokenAddress: String
): BigNumber | undefined => {
  const { chainId, account } = useEthers();
  const { abi } = tokenFarm;

  const tokenFarmAddress = networkMapping[String(chainId)]["TokenFarm"][0];

  const tokenFarmInterface = new utils.Interface(abi);
  const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

  const { value, error } =
    useCall(
      tokenAddress && {
        contract: tokenFarmContract,
        method: "tokenBalance",
        args: [tokenFarmAddress, account],
      }
    ) ?? {};

  if (error) {
    console.error(error.message);
    return undefined;
  }

  return value ? value[0] : 0;
};
