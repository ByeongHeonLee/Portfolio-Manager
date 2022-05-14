const express = require('express');
const router = express.Router();
const multer = require('multer');
const { User } = require("../models/User");
const { Board } = require("../models/Board")
const { auth } = require("../middleware/auth");

//=================================
//      회원게시판 포스팅
//=================================

let storage = multer.diskStorage({
    
    destination: (req, file, cb) => {//어디에 파일을 저장할지 설명.
        cb(null, 'uploads/')
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}_${file.originalname}`)
    },
    fileFilter: (req, file, cb) => {
        const ext = path.extname(file.originalname)
        if (ext !== '.jpg' || ext !== '.png') {
            return cb(res.status(400).end('jpg, png 파일만 첨부할 수 있습니다.'), false);
        }
        cb(null, true)
    }
})

const upload = multer({ storage: storage }).single("file")


router.post("/uploadfiles", (req, res) => {
//파일을 서버에 저장한다.
    upload(req, res, err => {
        if (err) {
            return res.json({ success: false, err })
        }
        return res.json({ success: true, filePath: res.req.file.path, fileName: res.req.file.filename })
    })
});

router.post("/post", (req, res) => {
//게시글 업로드
    const board = new Board(req.body)

    board.save((err, doc) => {
        if(err) return res.json({ success: false, err })
        res.status(200).json({ success: true })
    })
});

router.get("/getPosts", (req, res) => {
    //게시글을 db에서 가져와 테이블페이지에 보낸다.
       Board.find()
       .populate('writer')
       .exec((err, posts) => {
           if(err) return res.status(400).send(err);
           res.status(200).json({success: true, posts })
       })
    });


router.post("/getPostDetail", (req, res) => {
    Board.findOne({ "_id" : req.body.postId })
    .populate('writer')
    .exec((err, postDetail) => {
        if(err) return res.status(400).send(err)
        return res.status(200).json({ success: true, postDetail })
    })
});




//=================================
//             User
//=================================

router.get("/auth", auth, (req, res) => {
    res.status(200).json({
        _id: req.user._id,
        isAdmin: req.user.role === 0 ? false : true,
        isAuth: true,
        email: req.user.email,
        name: req.user.name,
        lastname: req.user.lastname,
        role: req.user.role,
        image: req.user.image,
    });
});

router.post("/register", (req, res) => {

    const user = new User(req.body);

    user.save((err, doc) => {
        if (err) return res.json({ success: false, err });
        return res.status(200).json({
            success: true
        });
    });
});

router.post("/login", (req, res) => {
    User.findOne({ email: req.body.email }, (err, user) => {
        if (!user)
            return res.json({
                loginSuccess: false,
                message: "Auth failed, email not found"
            });

        user.comparePassword(req.body.password, (err, isMatch) => {
            if (!isMatch)
                return res.json({ loginSuccess: false, message: "Wrong password" });

            user.generateToken((err, user) => {
                if (err) return res.status(400).send(err);
                res.cookie("w_authExp", user.tokenExp);
                res
                    .cookie("w_auth", user.token)
                    .status(200)
                    .json({
                        loginSuccess: true, userId: user._id
                    });
            });
        });
    });
});

router.get("/logout", auth, (req, res) => {
    User.findOneAndUpdate({ _id: req.user._id }, { token: "", tokenExp: "" }, (err, doc) => {
        if (err) return res.json({ success: false, err });
        return res.status(200).send({
            success: true
        });
    });
});

module.exports = router;
