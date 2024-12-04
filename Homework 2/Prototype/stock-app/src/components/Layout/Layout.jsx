import Header from "./Header";

const Layout = (props) => {
  return (
    <>
      <Header change={props.change} />
      {props.children}
    </>
  );
};

export default Layout;
