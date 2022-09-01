import React from "react";

const LoadingSpinner=({hidden}) => {
  return (
    <div className={(hidden ? "spinner-container" : "spinner-hidden")}>
      <div className="loading-spinner">
      </div>
    </div>
  );
}
export default LoadingSpinner;