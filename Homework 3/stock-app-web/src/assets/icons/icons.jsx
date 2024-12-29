export const StockUp = (props) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="rgb(22 101 52)"
      width={props.width} // Changed width to 24
      height={props.height} // Changed height to 24
      id="trending"
      viewBox="0 0 48 48"
    >
      <path d="m32 12 4.59 4.59-9.76 9.75-8-8L4 33.17 6.83 36l12-12 8 8 12.58-12.59L44 24V12z"></path>
      <path fill="none" d="M0 0h48v48H0z"></path>
    </svg>
  );
};
export const StockDown=(props)=>{
    return (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="rgb(153 27 27)"
        viewBox="0 0 24 24"
        width={props.width} // Changed width to 24
        height={props.height}
        id="down-growth"
          >
        <path d="M21,11a1,1,0,0,0-1,1v2.59l-6.29-6.3a1,1,0,0,0-1.42,0L9,11.59,3.71,6.29A1,1,0,0,0,2.29,7.71l6,6a1,1,0,0,0,1.42,0L13,10.41,18.59,16H16a1,1,0,0,0,0,2h5a1,1,0,0,0,.38-.08,1,1,0,0,0,.54-.54A1,1,0,0,0,22,17V12A1,1,0,0,0,21,11Z"></path>
      </svg>
    );
};

