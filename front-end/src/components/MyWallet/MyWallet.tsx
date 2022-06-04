import React from "react";
import { Token } from "../Main";
import {
  Box,
  Tab,
  Card,
  CardHeader,
  Divider,
  makeStyles,
} from "@material-ui/core";
import { TabContext, TabList, TabPanel } from "@material-ui/lab";
import { useState } from "react";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";
import { UnstakeForm } from "./UnstakeForm";
import { StakedBalance } from "./StakedBalance";

interface MyWalletProps {
  supportedTokens: Array<Token>;
}

const useStyles = makeStyles((theme) => ({
  card: {
    margin: `${theme.spacing(4)}px 0`,
    padding: theme.spacing(2),
  },
}));

export const MyWallet = ({ supportedTokens }: MyWalletProps) => {
  const [selectedTab, setSelectedTab] = useState(0);
  const classes = useStyles();
  console.log(supportedTokens);

  const tabChangeHandler = (event: React.ChangeEvent<{}>, newValue: string) => {
    setSelectedTab(parseInt(newValue));
  };

  return (
    <Box>
      <h1>Wallet</h1>
      <Box>
        <TabContext value={selectedTab.toString()}>
          <TabList onChange={tabChangeHandler} aria-label="stake from tabs">
            {supportedTokens.map((token, index) => {
              return (
                <Tab label={token.name} value={index.toString()} key={index} />
              );
            })}
          </TabList>
          {supportedTokens.map((token, index) => {
            return (
              <TabPanel value={index.toString()} key={index}>
                <Card className={classes.card}>
                  <CardHeader title="Stake" />
                  <WalletBalance token={supportedTokens[selectedTab]} />
                  <StakeForm token={supportedTokens[selectedTab]}></StakeForm>
                </Card>
                <Divider light />
                <Card className={classes.card}>
                  <CardHeader title="Unstake" />
                  <StakedBalance token={supportedTokens[selectedTab]} />
                  <UnstakeForm
                    token={supportedTokens[selectedTab]}
                  ></UnstakeForm>
                </Card>
              </TabPanel>
            );
          })}
        </TabContext>
      </Box>
    </Box>
  );
};
