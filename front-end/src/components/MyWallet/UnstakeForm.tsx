import { Input, Button, CircularProgress, Snackbar } from "@material-ui/core";
import { Alert } from "@material-ui/lab";
import { useEthers, useNotifications, useTokenBalance } from "@usedapp/core";
import React, { useEffect, useState } from "react";
import { useUnstakeToken } from "../../hooks/useUnstakeToken";
import { Token } from "../Main";

interface UnstakeFormProps {
  token: Token;
}

export const UnstakeForm = ({ token }: UnstakeFormProps) => {
  const { image, address, name } = token;
  const { account } = useEthers();
  const tokenBalance = useTokenBalance(address, account);
  const [unstakeAmount, setUnstakeAmount] = useState<number | string>("0");
  const [unstakeStatus, setUnstakeStatus] = useState(false);

  const setUnstakeAmountHandler = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const amt = event.target.value === "" ? "" : Number(event.target.value);
    setUnstakeAmount(amt);
  };

  const { unstakeERC20, unstakeERC20State } = useUnstakeToken();
  const isUnstaking = unstakeERC20State.status == "Mining";
  const { notifications } = useNotifications();

  const unstakeTokenHandler = () => {
    return unstakeERC20(address);
  };

  const closeSnackHandler = () => {
    unstakeStatus && setUnstakeStatus(false);
  };

  useEffect(() => {
    if (
      notifications.filter(
        (notification) =>
          notification.type == "transactionSucceed" &&
          notification.transactionName == "Unstake tokens"
      ).length > 0
    ) {
      setUnstakeStatus(true);
    }
  }, [notifications]);

  return (
    <>
      <Input onChange={setUnstakeAmountHandler} />
      <Button
        color="primary"
        size="large"
        onClick={unstakeTokenHandler}
        disabled={isUnstaking}
      >
        {isUnstaking ? <CircularProgress size={26} /> : "Unstake"}
      </Button>
      <Snackbar
        open={unstakeStatus}
        autoHideDuration={3000}
        onClose={closeSnackHandler}
      >
        <Alert onClose={closeSnackHandler} severity="success">
          Token successfully unstaked
        </Alert>
      </Snackbar>
    </>
  );
};
