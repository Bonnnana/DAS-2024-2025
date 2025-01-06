import Footer from "./Footer";
import Header from "./Header";

const Layout = (props) => {
  return (
    <div className="min-h-screen bg-primary relative">
      <Header change={props.change} />
      {props.children}
      <Footer/>
    </div>
  );
};

export default Layout;
