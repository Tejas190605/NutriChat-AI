import React from "react";
import { Dialog, DialogProps } from "./dialog";

export const Modal: React.FC<DialogProps> = (props) => {
  return <Dialog {...props} />;
};
