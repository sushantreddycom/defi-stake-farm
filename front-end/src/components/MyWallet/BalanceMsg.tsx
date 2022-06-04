import { makeStyles } from "@material-ui/core";
import { StakeForm } from "./StakeForm";

interface BalanceMsgProps {
  img: string;
  name: string;
  balance: number;
}

const useStyles = makeStyles((theme) => ({
  container: {
    display: "inline-grid",
    gridTemplateColumns: "auto auto auto",
    gap: theme.spacing(1),
    alignItems: "center",
  },
  tokenImg: {
    width: "32px",
  },
  amount: {
    fontWeight: 700,
  },
}));

export const BalanceMsg = (inputs: BalanceMsgProps) => {
  const { img, name, balance } = inputs;
  const classes = useStyles();

  return (
    <div className={classes.container}>
      <div>{`Your unstaked ${name} amount`}</div>
      <div className={classes.amount}>{balance}</div>
      <img className={classes.tokenImg} src={img} alt="token logo" />
    </div>
  );
};
