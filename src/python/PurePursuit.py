#!/usr/bin/python
# carlosrl@gmail.com - 08/08/2016

import numpy as np
import math

class PurePursuit:
	"""
	Implements the pure pursuit algorithm.
	Input: World path with way points to be followed by the robot
	"""
    def __init__(self, path):
        self.__wayPoints = path
        self.__pathLen = np.size(path, 0)
        self.__iway = 0
        self.__maxLinearVelocity = 1.0
        self.__maxAngularVelocity = 6.0
        self.__lookAheadDistance = 0.0
        self.__lookAheadPoint = np.zeros((1, 2))
        self.__goal = np.zeros((1, 2))
        self.__goal = path[1]
        self.__desiredLinearVelocity = .6
        self.__angularVelocity = 0
        self.__dist = 0
        self.__lastPose = np.zeros((1, 3))
        self.__isRunning = False
        self.__tolerance = 0.13
	
	# Calculate difference between 2 angles
    def angdiff(self, th1, th2):
        d = th1 - th2
        d = np.mod(d+np.pi, 2*np.pi) - np.pi
        return d

	# Set the distance between start and goal
    def setLookAheadDistance(self, curPos, goalPos):
        self.__lookAheadDistance = math.atan2(goalPos[1]-curPos[1], goalPos[0]-curPos[0])

	# Calculate distance between 2 points
    def calcDistance(self, P1, P2):
        x = math.sqrt((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2)
        return x

	# This function iterates across the entire way points
    def step(self, curPose):
        if curPose is not None:
            dist = self.calcDistance(curPose, self.__goal)
            self.__lastPose = curPose
            if dist < self.__tolerance:
                self.__isRunning = False

        if not self.__isRunning:
            self.__iway += 1
            while True:         # get the next valid point
                if self.__iway < self.__pathLen-1:
                    self.__lookAheadPoint = self.__wayPoints[self.__iway]
                    self.__goal = self.__wayPoints[self.__iway]
                else:
                    self.__lookAheadPoint = self.__wayPoints[self.__pathLen-1]
                    self.__goal = self.__wayPoints[self.__pathLen-1]
                dist = self.calcDistance(curPose, self.__goal)
                if dist < self.__tolerance:
                    self.__iway += 1
                else:
                # save distance
                    self.__lookAheadDistance = self.calcDistance(curPose, self.__goal)
                    break
            # get angle between rover heading and line path
            slope = math.atan2(self.__goal[1] - curPose[1], self.__goal[0] - curPose[0])
            alpha = self.angdiff(slope, curPose[2])

            # in this model, angular velocity is equal to desired curvature
            w = (2*np.sin(alpha))/self.__lookAheadDistance

            # use constant rotation when rover is running in negative path direction
            if np.abs(np.abs(alpha) - np.pi) < 10**(-12):
                w = np.sign(w)
            self.__angularVelocity = w
            self.__isRunning = True
        else:
            w = self.__angularVelocity

        v = self.__desiredLinearVelocity
        if np.abs(w) > self.__maxAngularVelocity:
            w = np.sign(w) * self.__maxAngularVelocity
            self.__angularVelocity = w
            v = .1
        return [v, w]




