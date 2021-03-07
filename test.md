# 汇编基础

## CPU如何知当前需要指行指令地址？
- 段寄存器`CS`和寄存器`IP`分别记录当前指令的段地址和偏移地址

## mov,add,sub指令
### mov
可用语法
- `mov 寄存器,数据 - mov ax,8`
- `mov 寄存器,寄存器 - mov ax,bx`
- `mov 寄存器,内存单元 - mov ax,[0]`
- `mov 内存单元,寄存器 - mov,[0],ax`
- `mov 段寄存器,寄存器 - mov ds,ax`

Q : 举一反三,是否存在 `mov 寄存器,段寄存器`呢?
- `mov 寄存器,段寄存器 - mov ax,ds`

Q : 是否存在`mov 段寄存器,内存单元`和`mov 内存单元,段寄存器`呢?
- `mov 段寄存器,内存单元 - mov ds,[0]` 
- `mov 内存单元,段寄存器 - mov [0],ds` 

综合以上
- `mov 寄存器,数据 - mov ax,8`
- `mov 寄存器,寄存器 - mov ax,bx`
- `mov 寄存器,内存单元 - mov ax,[0]`
- `mov 内存单元,寄存器 - mov,[0],ax`
- `mov 段寄存器,寄存器 - mov ds,ax`
- `mov 寄存器,段寄存器 - mov ax,ds`
- `mov 段寄存器,内存单元 - mov ds,[0]` 
- `mov 内存单元,段寄存器 - mov [0],ds` 

### add
可用语法
- `add 寄存器,数据 - add ax,8`
- `add 寄存器,寄存器 - add ax,bx`
- `add 寄存器,内存单元 - add ax,[0]`
- `add 内存单元,寄存器 - add [0],ax`

### sub
可用语法
- `sub 寄存器,数据 - sub ax,8`
- `sub 寄存器,寄存器 - sub ax,bx`
- `sub 寄存器,内存单元 - sub ax,[0]`
- `sub 内存单元,寄存器 - sub [0],ax`

## 栈及栈机制
- `push`入栈，`pop`出栈
- 遵循**后进先出(LIFO - Last in First Out)**
- 以**字**为单位
- 段寄存器`SS`,寄存器`SP`分别存储栈地址和偏移地址，**`SS:SP`始终指向栈顶**
- 栈顶从**高地址向低地址**方向增长

### 栈顶超界问题
- 8086CPU不保证栈顶不会超过栈空间

## push,pop指令

### 对寄存器
- `push 寄存器 - push ax` - 数据入栈
- `pop 寄存器 - pop ax` -  数据出栈

### 对段寄存器
- `push 段寄存器 - push ds` - 压入一个段寄存器的数据
- `pop 段寄存器 - pop ds` - 出栈，用一个段寄存器接受出栈数据

### 对内存单元
- `push 内存单元 - push [0]` - 压入内存单元字
- `pop 内存单元 - pop [0]` - 用一个内存字单元来接收出栈的字
> 注 : 8086CPU从`DS`中获取段地址

### 一些实例
```x86asm
; 3.7 : 以 10000H~1000FH 这段空间作为栈空间,将ax,bx,ds压入栈
    mov ax,1000H
    mov ss,ax; 设置栈的段地址不能直接传入数据,需用寄存器中转
    mov sp,0010H; 为什么是0010? 因为空栈的起点就在这
    push ax
    push bx
    push ds
```

```x86asm
; 3.8 : 
; 1.10000H~1000FH 作为栈空间,初始为空
; 2.设置ax=001AH,bx=001BH
; 3.依次压入栈
; 4.ax,bx置零
; 5.从栈中恢复ax,bx
    mov ax,1000H
    mov ss,ax
    mov sp,0100H; 1.栈空间初始化完成
    mov ax,001AH
    mov bx,001BH; 2.置值完成
    push ax
    push bx; 3.入栈完成
    mov ax,0000H; sub ax,ax 机器码只占2字效率更高
    mov bx,0000H; 4.置零完成
    pop bx
    pop ax; 5.恢复完成
```

## 栈的综述
- `SS`,`SP`存放栈顶的段地址和偏移地址 提供`push`,`pop`来以栈的方式访问内存单元
- `push`指令执行步骤
> 1. `SP = SP - 2`
> 2. 向`SS:SP`指向的内存地址传送数据
- `SS:SP`始终指向栈顶
- 8086CPU只记录栈顶,栈大小的空间需要自己管理
- 后进先出 LIFO (Last In First Out)
- `push`和`pop`不局限于栈,它实质上是内存传送指令

## 栈段
- 关于最大栈段
```x86asm
    mov ax,FFFEH
    add ax,0002H; ax=0000H
```
- 明显，最大栈段为64KB `(FFFFH+1D)/1024=64KB`

## 段的综述
- **数据段** - 存放数据,段地址存放于`DS`
- **代码段** - 存放代码,段地址存放于`CS`,偏移地址存放于`IP`
- **栈段** - 作为栈,段地址存放于`SS`,偏移地址存放于`SP`
  
