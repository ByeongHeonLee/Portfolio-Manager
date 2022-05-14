import React from 'react';
import { Menu } from 'antd';
// const SubMenu = Menu.SubMenu;
// const MenuItemGroup = Menu.ItemGroup;

function LeftMenu(props) {
  return (
    <Menu mode={props.mode}>
    {/* <Menu.Item key="mail">
      <a href="/">Home</a>
    </Menu.Item> */}
       <Menu.Item key="board">
          <a href="/board">토론게시판</a>
        </Menu.Item>
        <Menu.Item key="sim">
          <a href="/simulate">모의투자</a>
        </Menu.Item>
  </Menu>
  )
}

export default LeftMenu