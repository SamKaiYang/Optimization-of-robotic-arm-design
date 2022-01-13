;; Auto-generated. Do not edit!


(when (boundp 'interface_control::cal_cmd)
  (if (not (find-package "INTERFACE_CONTROL"))
    (make-package "INTERFACE_CONTROL"))
  (shadow 'cal_cmd (find-package "INTERFACE_CONTROL")))
(unless (find-package "INTERFACE_CONTROL::CAL_CMD")
  (make-package "INTERFACE_CONTROL::CAL_CMD"))

(in-package "ROS")
;;//! \htmlinclude cal_cmd.msg.html


(defclass interface_control::cal_cmd
  :super ros::object
  :slots (_cmd ))

(defmethod interface_control::cal_cmd
  (:init
   (&key
    ((:cmd __cmd) 0)
    )
   (send-super :init)
   (setq _cmd (round __cmd))
   self)
  (:cmd
   (&optional __cmd)
   (if __cmd (setq _cmd __cmd)) _cmd)
  (:serialization-length
   ()
   (+
    ;; int32 _cmd
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _cmd
       (write-long _cmd s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _cmd
     (setq _cmd (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get interface_control::cal_cmd :md5sum-) "66990e73c7aab0c47ddcdc70f7fa5bd0")
(setf (get interface_control::cal_cmd :datatype-) "interface_control/cal_cmd")
(setf (get interface_control::cal_cmd :definition-)
      "int32 cmd
")



(provide :interface_control/cal_cmd "66990e73c7aab0c47ddcdc70f7fa5bd0")


