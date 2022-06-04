import React from "react";
import { useEthers } from "@usedapp/core";
import helperConfig from "../helper-config.json";
import networkMapping from "../chain-info/deployments/map.json";
import brownieConfig from "../brownie-config.json";
import { constants } from "ethers";
import eth from "../components/Images/eth.png";
import dai from "../components/Images/dai.png";
import dapp from "../components/Images/dapp.png";
import { MyWallet } from "./MyWallet/MyWallet";

export type Token = {
  image: string;
  address: string;
  name: string;
};

const Main = () => {
  // show token values from wallet
  // get address of different tokens
  // get balance of users wallet

  const { chainId, error } = useEthers();
  const networkName = chainId ? helperConfig[String(chainId)] : "dev";

  const cheruTokenAddress = chainId
    ? networkMapping[String(chainId)]["CheruToken"][0]
    : constants.AddressZero;

  const tokenFarmAddress = chainId
    ? networkMapping[String(chainId)]["TokenFarm"]
    : constants.AddressZero;

  const wethTokenAddress = chainId
    ? brownieConfig["networks"][networkName]["weth_token"]
    : constants.AddressZero;

  const fauTokenAddress = chainId
    ? brownieConfig["networks"][networkName]["fau_token"]
    : constants.AddressZero;

  const daiTokenAddress = chainId
    ? brownieConfig["networks"][networkName]["dai_token"]
    : constants.AddressZero;

  console.log("chain id=", chainId);
  console.log("network name=", networkName);

  const supportedTokens: Array<Token> = [
    {
      image: eth,
      address: wethTokenAddress,
      name: "WETH",
    },
    {
      image: dai,
      address: fauTokenAddress,
      name: "DAI",
    },
    {
      image: dapp,
      address: cheruTokenAddress,
      name: "CHE",
    },
  ];

  return <MyWallet supportedTokens={supportedTokens} />;
};

export default Main;
