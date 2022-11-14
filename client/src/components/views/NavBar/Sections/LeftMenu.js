import React from 'react';
import { Menu } from 'antd';
import './Navbar.css'
// const SubMenu = Menu.SubMenu;
// const MenuItemGroup = Menu.ItemGroup;

function LeftMenu(props) {
  return (
    <Menu mode={props.mode}>
    {/* <Menu.Item key="mail">
      <a href="/">Home</a>
    </Menu.Item> */}
        <Menu.Item key="search">
          <a href="/search">종목검색</a>
        </Menu.Item>
        <Menu.Item key="worldIndex">
          <a href="/index">세계지수</a>
        </Menu.Item>
        <Menu.Item key="board">
          <a href="/board">토론게시판</a>
        </Menu.Item>
        {/* <Menu.Item key="sim">
          <a href="/simulate">모의투자</a>
        </Menu.Item> */}
  </Menu>
  )
}

export default LeftMenu
