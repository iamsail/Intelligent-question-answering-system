<?php
/**
 * Created by PhpStorm.
 * User: sail
 * Date: 18-6-25
 * Time: 上午12:48
 */

namespace App\Http\Controllers;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
class AppController
{

    /**
     * 获取所有QA对
     *
     * @return {array}　$arr  QA对
     */
    public function getQA() {
        $arr = array();
        $arr['QA'] = DB::select('select * from all_QA');
        return $arr;
    }

    /**
     * 用户登录
     *　
     * @param  {Request} $request 用户请求
     * @return {number}　$final  状态码　0 用户不存在; 1　登录成功; 2　密码错误;3 用户已经登录;
     */
    public function login(Request $request) {
        $input = $request->all();
        $result = DB::select('select * from admin where username = ?', [$input['username']]);
        $final = null;
        if ($this->isUserLogin()) {
            $final = 3;
        } else {
            if ($result == null) {
                $final = 0;
            } elseif ($result[0] -> password == $input['password']) {
                session(['username' => $input['username']]);
                $final  = 1;
            } else {
                $final  = 2;
            }
        }

        return $final;
    }


    /**
     * 用户是否已经登录
     *　
     * @return boolean
     */
    protected function isUserLogin() {
        $sessionName = session('username');
        if ($sessionName) {
            return true;
        }
        return false;
    }

    /**
     * 获取用户名
     *　
     * @return {String} $username　用户名
     */
    public function getUsername() {
        $username = session('username');
        if (!$username) {
            $username = '游客';
        }
        return $username;
    }

    /**
     * 用户登出
     *　
     * @param  {Request} $request 用户请求
     */
    public function logout(Request $request) {
        $request->session()->flush();
        return $this->getUsername();
    }
}